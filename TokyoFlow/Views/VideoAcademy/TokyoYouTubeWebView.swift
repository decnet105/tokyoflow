import SwiftUI
import WebKit

public struct TokyoYouTubeWebView: UIViewRepresentable {
    public let videoId: String
    public var onPlaybackProgress: ((Double) -> Void)? = nil

    public init(videoId: String, onPlaybackProgress: ((Double) -> Void)? = nil) {
        self.videoId = videoId
        self.onPlaybackProgress = onPlaybackProgress
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    public func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.scrollView.isScrollEnabled = false
        webView.backgroundColor = .black
        webView.isOpaque = false

        loadYouTubeIFrame(webView: webView, videoId: videoId)
        return webView
    }

    public func updateUIView(_ uiView: WKWebView, context: Context) {
        // Only reload if video changed
        if context.coordinator.currentVideoId != videoId {
            context.coordinator.currentVideoId = videoId
            loadYouTubeIFrame(webView: uiView, videoId: videoId)
        }
    }

    private func loadYouTubeIFrame(webView: WKWebView, videoId: String) {
        let embedHtml = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body, html { width: 100%; height: 100%; background-color: #000; overflow: hidden; }
                iframe { width: 100%; height: 100%; border: none; }
            </style>
        </head>
        <body>
            <iframe id="player"
                src="https://www.youtube-nocookie.com/embed/\(videoId)?enablejsapi=1&playsinline=1&rel=0&modestbranding=1&autoplay=0&origin=https://www.youtube.com"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen>
            </iframe>
        </body>
        </html>
        """
        webView.loadHTMLString(embedHtml, baseURL: URL(string: "https://www.youtube.com"))
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
