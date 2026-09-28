import Foundation
import AppKit
import Vision
import PDFKit

// MARK: - Book OCR Extractor & English Curriculum Builder
struct RawVocabEntry {
    var kanji: String
    var reading: String
    var romaji: String
    var pitch: String
    var level: String
    var pos: String
    var meaning: String
    var exampleJa: String
    var exampleEn: String
    var tag: String
}

let bookPath = "/Users/kilvonwu/Documents/books/红宝书大全集 新日本语能力考试N1-N5文字词汇详解 精装纪念版 (许小明，Reika主编；新世界图书事业部刘学敏，陈晓宇，钟雁，张蕾，凌瑾怡，吴秀华... (z-library.sk, 1lib.sk, z-lib.sk).pdf"
let url = URL(fileURLWithPath: bookPath)
guard let pdfDoc = PDFDocument(url: url) else {
    print("❌ Could not open PDF")
    exit(1)
}

print("📖 Opened Hongbaoshu (Total Pages: \(pdfDoc.pageCount))")

// Define sample page spans for each level to extract deep curricula
// N1: pages 20-170, N2: pages 185-305, N3: pages 315-435, N4: pages 445-505, N5: pages 515-575
let levelPageRanges: [(level: String, range: [Int])] = [
    ("N1", Array(stride(from: 20, through: 170, by: 4))),
    ("N2", Array(stride(from: 185, through: 305, by: 4))),
    ("N3", Array(stride(from: 315, through: 435, by: 4))),
    ("N4", Array(stride(from: 445, through: 505, by: 3))),
    ("N5", Array(stride(from: 515, through: 575, by: 3)))
]

var extractedEntries: [RawVocabEntry] = []

let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["ja-JP", "zh-Hans", "en-US"]
request.recognitionLevel = .accurate

for (level, pages) in levelPageRanges {
    print("🔍 Processing OCR for \(level) across \(pages.count) pages...")
    for p in pages {
        guard let page = pdfDoc.page(at: p) else { continue }
        let pageRect = page.bounds(for: .mediaBox)
        let image = page.thumbnail(of: CGSize(width: pageRect.width * 1.8, height: pageRect.height * 1.8), for: .mediaBox)
        guard let tiff = image.tiffRepresentation,
              let rep = NSBitmapImageRep(data: tiff),
              let cg = rep.cgImage else { continue }
        
        let handler = VNImageRequestHandler(cgImage: cg, options: [:])
        try? handler.perform([request])
        guard let results = request.results else { continue }
        
        let lines = results.compactMap { $0.topCandidates(1).first?.string }
        
        // Parse lines for headwords like "口 移住（いじゅう）⓪［名・自動3］" or "移住（いじゅう）"
        var currentKanji = ""
        var currentReading = ""
        var currentPitch = "[0] Heiban"
        var currentPos = "Noun / Suru-Verb"
        var currentExJa = ""
        
        for i in 0..<lines.count {
            let line = lines[i]
            
            // Look for pattern containing （...）
            if let openParen = line.firstIndex(of: "（"),
               let closeParen = line.firstIndex(of: "）"),
               openParen < closeParen {
                
                let headwordPart = String(line[..<openParen]).replacingOccurrences(of: "口", with: "").replacingOccurrences(of: "ロ", with: "").trimmingCharacters(in: .whitespaces)
                let readingPart = String(line[line.index(after: openParen)..<closeParen]).trimmingCharacters(in: .whitespaces)
                
                if !headwordPart.isEmpty && !readingPart.isEmpty && headwordPart.count <= 6 {
                    currentKanji = headwordPart
                    currentReading = readingPart
                    
                    // Pitch accent check
                    if line.contains("①") || line.contains("1") {
                        currentPitch = "[1] Atamadaka"
                    } else if line.contains("②") || line.contains("2") {
                        currentPitch = "[2] Nakadaka"
                    } else if line.contains("③") || line.contains("3") {
                        currentPitch = "[3] Nakadaka"
                    } else if line.contains("④") || line.contains("4") {
                        currentPitch = "[4] Odaka"
                    } else {
                        currentPitch = "[0] Heiban"
                    }
                    
                    // POS check
                    if line.contains("自動") {
                        currentPos = "Godan/Ichidan Verb (Intransitive)"
                    } else if line.contains("他動") {
                        currentPos = "Godan/Ichidan Verb (Transitive)"
                    } else if line.contains("イ形") {
                        currentPos = "I-Adjective"
                    } else if line.contains("ナ形") {
                        currentPos = "Na-Adjective"
                    } else if line.contains("副") {
                        currentPos = "Adverb"
                    } else {
                        currentPos = "Noun / Suru-Verb"
                    }
                    
                    // Look ahead for example sentence
                    if i + 1 < lines.count {
                        let nextLine = lines[i+1]
                        if nextLine.contains("。") || nextLine.contains("／") || nextLine.contains("/") {
                            let parts = nextLine.components(separatedBy: CharacterSet(charactersIn: "/／"))
                            currentExJa = parts.first?.replacingOccurrences(of: "A", with: "").replacingOccurrences(of: "▶", with: "").trimmingCharacters(in: .whitespaces) ?? ""
                        }
                    }
                    
                    if currentExJa.isEmpty {
                        currentExJa = "\(currentKanji)を使って会話する。"
                    }
                    
                    extractedEntries.append(RawVocabEntry(
                        kanji: currentKanji,
                        reading: currentReading,
                        romaji: currentReading, // will be romanized
                        pitch: currentPitch,
                        level: level,
                        pos: currentPos,
                        meaning: "", // will be translated to English
                        exampleJa: currentExJa,
                        exampleEn: "",
                        tag: level == "N1" || level == "N2" ? "business" : (level == "N3" ? "social" : "daily")
                    ))
                }
            }
        }
    }
}

print("✅ OCR extracted \(extractedEntries.count) raw candidates from Hongbaoshu.")

// Save raw extracted entries to JSON for enrichment
struct OCRResult: Codable {
    let kanji: String
    let reading: String
    let pitch: String
    let level: String
    let pos: String
    let exampleJa: String
}

let ocrOutput = extractedEntries.map { OCRResult(kanji: $0.kanji, reading: $0.reading, pitch: $0.pitch, level: $0.level, pos: $0.pos, exampleJa: $0.exampleJa) }
let outData = try! JSONEncoder().encode(ocrOutput)
try! outData.write(to: URL(fileURLWithPath: "scripts/raw_ocr_extracted.json"))
print("💾 Saved raw OCR entries to scripts/raw_ocr_extracted.json")
