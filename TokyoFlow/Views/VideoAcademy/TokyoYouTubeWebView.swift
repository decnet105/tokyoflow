import SwiftUI
import WebKit
import SafariServices

public struct TokyoYouTubeWebView: UIViewRepresentable {
    public let videoId: String
    public var autoPlay: Bool = false
    public var onPlaybackProgress: ((Double) -> Void)? = nil

    public init(videoId: String, autoPlay: Bool = false, onPlaybackProgress: ((Double) -> Void)? = nil) {
        self.videoId = videoId
        self.autoPlay = autoPlay
        self.onPlaybackProgress = onPlaybackProgress
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    public func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        config.allowsPictureInPictureMediaPlayback = true
        config.allowsAirPlayForMediaPlayback = true
        config.defaultWebpagePreferences.allowsContentJavaScript = true
        config.applicationNameForUserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.scrollView.isScrollEnabled = false
        webView.backgroundColor = .black
        webView.isOpaque = false

        loadFastEmbed(webView: webView, videoId: videoId, autoPlay: autoPlay)
        return webView
    }

    public func updateUIView(_ uiView: WKWebView, context: Context) {
        if context.coordinator.currentVideoId != videoId {
            context.coordinator.currentVideoId = videoId
            loadFastEmbed(webView: uiView, videoId: videoId, autoPlay: autoPlay)
        }
    }

    private func loadFastEmbed(webView: WKWebView, videoId: String, autoPlay: Bool) {
        let playFlag = autoPlay ? 1 : 0
        let embedHtml = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <link rel="preconnect" href="https://www.youtube.com" crossorigin>
            <link rel="preconnect" href="https://www.youtube-nocookie.com" crossorigin>
            <link rel="preconnect" href="https://i.ytimg.com" crossorigin>
            <link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body, html { width: 100%; height: 100%; background: #000; overflow: hidden; }
                iframe { width: 100%; height: 100%; border: 0; }
            </style>
        </head>
        <body>
            <iframe id="player"
                src="https://www.youtube-nocookie.com/embed/\(videoId)?playsinline=1&autoplay=\(playFlag)&rel=0&modestbranding=1&controls=1&iv_load_policy=3&fs=1&enablejsapi=1"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen>
            </iframe>
        </body>
        </html>
        """
        webView.loadHTMLString(embedHtml, baseURL: URL(string: "https://www.youtube-nocookie.com"))
    }

    public class Coordinator: NSObject, WKNavigationDelegate {
        var parent: TokyoYouTubeWebView
        var currentVideoId: String = ""

        init(_ parent: TokyoYouTubeWebView) {
            self.parent = parent
            self.currentVideoId = parent.videoId
        }
    }
}

// MARK: - Instant Fast Thumbnail & Player Container
public struct TokyoFastVideoPlayerContainer: View {
    public let videoId: String
    public let title: String
    public let durationLabel: String
    @State private var isPlayerActive: Bool = false
    @Environment(\.openURL) private var openURL

    public init(videoId: String, title: String = "", durationLabel: String = "") {
        self.videoId = videoId
        self.title = title
        self.durationLabel = durationLabel
    }

    public var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.black)
                .aspectRatio(16/9, contentMode: .fit)

            if isPlayerActive {
                TokyoYouTubeWebView(videoId: videoId, autoPlay: true)
                    .cornerRadius(16)
                    .transition(.opacity)
            } else {
                // Instant HD Poster & Glowing Play Button (0ms load)
                ZStack {
                    AsyncImage(url: URL(string: "https://img.youtube.com/vi/\(videoId)/hqdefault.jpg")) { phase in
                        if let img = phase.image {
                            img.resizable()
                               .aspectRatio(16/9, contentMode: .fill)
                        } else {
                            LinearGradient(
                                colors: [Color(hex: "#1E293B"), Color(hex: "#0F172A")],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        }
                    }
                    .cornerRadius(16)

                    // Overlay Vignette
                    Color.black.opacity(0.35)
                        .cornerRadius(16)

                    // Glowing Play Button
                    Button(action: {
                        withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                            isPlayerActive = true
                        }
                    }) {
                        ZStack {
                            Circle()
                                .fill(Color.red)
                                .frame(width: 58, height: 58)
                                .shadow(color: Color.red.opacity(0.6), radius: 14, x: 0, y: 4)

                            Image(systemName: "play.fill")
                                .font(.system(size: 24, weight: .black))
                                .foregroundColor(.white)
                                .offset(x: 2)
                        }
                    }
                    .buttonStyle(.plain)

                    // Bottom info pills
                    VStack {
                        Spacer()
                        HStack {
                            if !durationLabel.isEmpty {
                                Text(durationLabel)
                                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.black.opacity(0.75))
                                    .cornerRadius(6)
                            }
                            Spacer()
                            HStack(spacing: 4) {
                                Image(systemName: "bolt.fill")
                                    .foregroundColor(.yellow)
                                    .font(.system(size: 10))
                                Text("0-Lag Stream")
                                    .font(.system(size: 10, weight: .bold))
                                    .foregroundColor(.white)
                            }
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.black.opacity(0.75))
                            .cornerRadius(6)
                        }
                        .padding(10)
                    }
                }
                .cornerRadius(16)
            }
        }
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.25), radius: 8, x: 0, y: 4)
    }
}
