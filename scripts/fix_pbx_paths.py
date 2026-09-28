import os
import re

pbx_path = "TokyoFlow.xcodeproj/project.pbxproj"
pbx = open(pbx_path, "r", encoding="utf-8").read()

# Let's inspect the file references for the new files
# We can set their path to:
# JLPTWord.swift -> Models/JLPTWord.swift or path = JLPTWord.swift within Models group
# In TokyoFlow project structure, groups have paths like `path = Models;`, `path = Services;`, `path = Views;`

# Let's clean up any incorrect entries first
files_map = {
    "JLPTWord.swift": ("Models", "../Models/JLPTWord.swift"),
    "JLPTDictionaryService.swift": ("Services", "JLPTDictionaryService.swift"),
    "WeakWordTrackerService.swift": ("Services", "WeakWordTrackerService.swift"),
    "SubscriptionService.swift": ("Services", "SubscriptionService.swift"),
    "JLPTDictionaryView.swift": ("Views", "../Views/Dictionary/JLPTDictionaryView.swift"),
    "WeakWordsLabView.swift": ("Views", "../Views/Dictionary/WeakWordsLabView.swift"),
    "TokyoProUpgradeModalView.swift": ("Views", "../Views/Subscription/TokyoProUpgradeModalView.swift"),
    "jlpt_dictionary.json": ("Resources", "jlpt_dictionary.json")
}

for fname, (grp, rel_path) in files_map.items():
    # Fix the fileRef path
    pattern = rf'(/\* {re.escape(fname)} \*/ = \{{isa = PBXFileReference;.*?path = )([^;]+)(; sourceTree = "<group>"; \}};)'
    def repl(m):
        return f'{m.group(1)}{rel_path}{m.group(3)}'
    pbx = re.sub(pattern, repl, pbx)

open(pbx_path, "w", encoding="utf-8").write(pbx)
print("Updated pbxproj paths successfully.")
