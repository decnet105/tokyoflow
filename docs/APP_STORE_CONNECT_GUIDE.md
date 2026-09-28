# 📱 TokyoFlow Japanese • App Store Connect (ASC) 发布审批手册

---

## 📌 1. 应用基本信息配置 (App Store Information)

- **App Name (应用名称)**: `TokyoFlow Japanese: Real Audio`
- **Subtitle (副标题)**: `Master Real-Life Tokyo Japanese` (30 字符以内)
- **Primary Category (主分类)**: `Education` (教育)
- **Secondary Category (次分类)**: `Travel` (旅游) 或 `Reference` (参考)
- **Bundle ID**: `com.tokyoflow.app`
- **Development Team**: `X5L4GA7WZP` (与 Mystory 完全一致的 Apple Developer ID)
- **SKU**: `tokyoflow_ios_v1`
- **Primary Language (主语言)**: `English (U.S.)`

---

## 📝 2. App Store 英文文案与描述 (Copy-Paste Ready)

### Promotional Text (宣传文本 - 可随时修改)
```text
Master real-life Tokyo Japanese with authentic train announcements, kombini survival phrases, izakaya etiquette, and NHK news audio shadowing!
```

### Full Description (完整应用介绍)
```text
TokyoFlow Japanese is your ultimate companion for mastering genuine, everyday Tokyo Japanese. 

Traditional textbooks teach polite, stiff Japanese you rarely hear in real Tokyo life. TokyoFlow bridges the gap with authentic subway broadcasts, convenience store checkout drills, izakaya dining etiquette, and NHK daily news shadowing.

✨ KEY FEATURES:

1. 🚇 TOKYO SCENARIO MASTERCLASS:
• Real-life audio breakdowns for Yamanote Line & Tokyo Metro platform announcements.
• 1-second survival response phrases for 7-Eleven, FamilyMart & Lawson registers.
• Showa izakaya ordering etiquette, sake customs, and casual slang.

2. 🎙️ NHK DAILY NEWS & NATIVE SHADOWING:
• Practice listening and speaking with simplified NHK Easy Japanese broadcasts.
• Millisecond-accurate prosody alignment and pitch accent guides.

3. 📖 JLPT N5–N1 CORE LEXICON:
• Searchable dictionary with kanji, hiragana, romaji, and contextual English glosses.
• Interactive SRS flashcards for smart spaced repetition.

4. 🎌 KANA TRAINER & MANGA LAB:
• Complete Hiragana & Katakana stroke order, audio pronunciations, and 7-day vocabulary memory charts.
• Decode real manga sound effects (onomatopoeia) and casual character speech.

5. ⚡ DOJO SPEED DRILLS & CITIZEN CHAT:
• Rapid-fire conversational decision drills.
• Chat with authentic Tokyo personas (Shibuya Gal, Izakaya Master, Station Clerk, Anime Otaku).

Start your Tokyo immersion journey today and speak Japanese with genuine confidence!
```

### Keywords (搜索关键词 - 100 字符以内，英文逗号分隔，勿留空格)
```text
japanese,learn japanese,tokyo,jlpt,n5,n4,n3,nihongo,hiragana,katakana,kanji,kombini,shadowing,yamanote
```

### Support & Privacy URLs
- **Support URL (技术支持网址)**: `https://tokyoflow.app/support`
- **Marketing URL (营销网址)**: `https://tokyoflow.app`
- **Privacy Policy URL (隐私政策网址)**: `https://tokyoflow.app/privacy`

---

## 🛠️ 3. 一键打包与上传到 App Store Connect 步骤

### 第一步：在 Xcode 中构建 Archive
```bash
# 1. 清理并运行测试确保 100% 成功
xcodebuild test -project TokyoFlow.xcodeproj -scheme TokyoFlow -destination 'platform=iOS Simulator,name=iPhone 17 Pro'

# 2. 生成发布归档 (Archive)
xcodebuild archive \
  -project TokyoFlow.xcodeproj \
  -scheme TokyoFlow \
  -configuration Release \
  -archivePath build/TokyoFlow.xcarchive
```

### 第二步：在 Xcode Organizer 或 Transporter 上传
1. 打开 Xcode -> 顶部菜单 **Window** -> **Organizer**。
2. 选中最新生成的 `TokyoFlow` 归档版本。
3. 点击右侧 **「Distribute App」** -> 选择 **「App Store Connect」** -> **「Upload」**。
4. 勾选 **Automatically manage signing**，点击上传。
5. 上传完成后，约 5~10 分钟即可在 [App Store Connect (appstoreconnect.apple.com)](https://appstoreconnect.apple.com/) 的 **TestFlight** 标签页中看到构建版本。

---

## 🔒 4. 视频私享（Private / Unlisted）策略说明

- **当前状态**：YouTube 上的 3 支视频保持 **Private (私享)** 或 **Unlisted (不公开列出)**，外部观众无法搜索或浏览到。
- **App 审核策略**：苹果审核人员在审查 iOS App 的 Video Academy 模块时，App 内部通过内置的播放器与离线教研资料即可顺畅体验全部场景精讲。
- **上线时间线**：
  1. iOS App 提交 ASC 审核并通过发布。
  2. 审核通过后，将 YouTube 上的 3 支视频一键设为 **Public (公开)**。
  3. YouTube 视频观众立即被引流至 App Store 下载 App，形成正向增长飞轮！
