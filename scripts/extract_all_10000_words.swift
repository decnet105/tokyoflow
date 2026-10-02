import Foundation
import AppKit
import Vision
import PDFKit

struct RawEntry: Codable {
    var kanji: String
    var reading: String
    var pitch: String
    var level: String
    var pos: String
    var exampleJa: String
}

let bookPath = "/Users/kilvonwu/Documents/books/超值白金版 红宝书大全集 新日本语能力考试N1-N5文字词汇详解 最新修订版 第2版 (许小明,(日)REIKA主编新世界图书事业部编著, 许小明, Reika主编 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
let url = URL(fileURLWithPath: bookPath)
guard let pdfDoc = PDFDocument(url: url) else {
    print("❌ Failed to open PDF: \(bookPath)")
    exit(1)
}

print("📖 Opened 《红宝书大全集》 Total Pages: \(pdfDoc.pageCount)")

// Define level boundaries
func levelForPage(_ p: Int) -> String {
    if p >= 15 && p <= 175 { return "N1" }
    if p >= 176 && p <= 310 { return "N2" }
    if p >= 311 && p <= 440 { return "N3" }
    if p >= 441 && p <= 510 { return "N4" }
    if p >= 511 && p <= 580 { return "N5" }
    return "N1"
}

let startPage = 15
let endPage = min(580, pdfDoc.pageCount - 1)
let totalPagesToProcess = endPage - startPage + 1
print("🚀 Starting High-Throughput Vision OCR across pages \(startPage) to \(endPage) (\(totalPagesToProcess) pages)...")

var allExtracted: [RawEntry] = []
let lock = NSLock()

DispatchQueue.concurrentPerform(iterations: totalPagesToProcess) { idx in
    let pageNum = startPage + idx
    guard let page = pdfDoc.page(at: pageNum) else { return }
    let level = levelForPage(pageNum)
    
    let pageRect = page.bounds(for: .mediaBox)
    let image = page.thumbnail(of: CGSize(width: pageRect.width * 2.0, height: pageRect.height * 2.0), for: .mediaBox)
    guard let tiff = image.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let cg = rep.cgImage else { return }
    
    let request = VNRecognizeTextRequest()
    request.recognitionLanguages = ["ja-JP", "zh-Hans", "en-US"]
    request.recognitionLevel = .accurate
    
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([request])
    guard let results = request.results else { return }
    
    let lines = results.compactMap { $0.topCandidates(1).first?.string }
    var pageEntries: [RawEntry] = []
    
    for i in 0..<lines.count {
        let line = lines[i]
        
        if let openParen = line.firstIndex(of: "（") ?? line.firstIndex(of: "("),
           let closeParen = line.firstIndex(of: "）") ?? line.firstIndex(of: ")"),
           openParen < closeParen {
            
            let headword = String(line[..<openParen])
                .replacingOccurrences(of: "口", with: "")
                .replacingOccurrences(of: "ロ", with: "")
                .replacingOccurrences(of: "■", with: "")
                .replacingOccurrences(of: "★", with: "")
                .trimmingCharacters(in: .whitespaces)
            let reading = String(line[line.index(after: openParen)..<closeParen]).trimmingCharacters(in: .whitespaces)
            
            if !headword.isEmpty && !reading.isEmpty && headword.count <= 8 {
                var pitch = "[0] Heiban"
                if line.contains("①") || line.contains("1") { pitch = "[1] Atamadaka" }
                else if line.contains("②") || line.contains("2") { pitch = "[2] Nakadaka" }
                else if line.contains("③") || line.contains("3") { pitch = "[3] Nakadaka" }
                else if line.contains("④") || line.contains("4") { pitch = "[4] Odaka" }
                else if line.contains("⑤") || line.contains("5") { pitch = "[5] Nakadaka" }
                
                var pos = "Noun / Suru-Verb"
                if line.contains("自動") { pos = "Godan/Ichidan Verb (Intransitive)" }
                else if line.contains("他動") { pos = "Godan/Ichidan Verb (Transitive)" }
                else if line.contains("動") { pos = "Verb" }
                else if line.contains("イ形") || line.contains("形1") { pos = "I-Adjective" }
                else if line.contains("ナ形") || line.contains("形2") { pos = "Na-Adjective" }
                else if line.contains("副") { pos = "Adverb" }
                else if line.contains("接") { pos = "Conjunction" }
                
                var exJa = ""
                if i + 1 < lines.count {
                    let nextLine = lines[i+1]
                    if nextLine.contains("。") || nextLine.contains("／") || nextLine.contains("/") {
                        let parts = nextLine.components(separatedBy: CharacterSet(charactersIn: "/／"))
                        exJa = parts.first?.replacingOccurrences(of: "A", with: "").replacingOccurrences(of: "▶", with: "").trimmingCharacters(in: .whitespaces) ?? ""
                    }
                }
                if exJa.isEmpty {
                    exJa = "\(headword)を使って会話する。"
                }
                
                pageEntries.append(RawEntry(
                    kanji: headword,
                    reading: reading,
                    pitch: pitch,
                    level: level,
                    pos: pos,
                    exampleJa: exJa
                ))
            }
        }
    }
    
    lock.lock()
    allExtracted.append(contentsOf: pageEntries)
    if allExtracted.count % 500 < 20 {
        print("  ⚡ Progress: \(allExtracted.count) words extracted so far (Page \(pageNum)/\(endPage))...")
    }
    lock.unlock()
}

print("✅ Finished Vision OCR! Total raw entries extracted: \(allExtracted.count)")

// Save raw entries to JSON
let outData = try JSONEncoder().encode(allExtracted)
let outUrl = URL(fileURLWithPath: "scripts/raw_ocr_full_10000.json")
try outData.write(to: outUrl)
print("💾 Saved full raw dataset to: \(outUrl.path)")
