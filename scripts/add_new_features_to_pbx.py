import os
import re

pbx_path = "TokyoFlow.xcodeproj/project.pbxproj"
pbx = open(pbx_path, "r", encoding="utf-8").read()

files_to_add = [
    # (FileName, RelativePath, GroupName, IsResource)
    ("jlpt_dictionary.json", "jlpt_dictionary.json", "Resources", True),
    ("JLPTWord.swift", "JLPTWord.swift", "Models", False),
    ("JLPTDictionaryService.swift", "JLPTDictionaryService.swift", "Services", False),
    ("WeakWordTrackerService.swift", "WeakWordTrackerService.swift", "Services", False),
    ("SubscriptionService.swift", "SubscriptionService.swift", "Services", False),
    ("JLPTDictionaryView.swift", "JLPTDictionaryView.swift", "Views", False),
    ("WeakWordsLabView.swift", "WeakWordsLabView.swift", "Views", False),
    ("TokyoProUpgradeModalView.swift", "TokyoProUpgradeModalView.swift", "Views", False),
]

import hashlib

for fname, fpath, group, is_res in files_to_add:
    fref_id = "FR_" + hashlib.md5(fname.encode()).hexdigest()[:20].upper()
    bld_id = "BL_" + hashlib.md5(fname.encode()).hexdigest()[:20].upper()

    if fref_id in pbx:
        print(f"Skipping {fname}, already present.")
        continue

    # PBXBuildFile
    phase = "Resources" if is_res else "Sources"
    bld_entry = f"\t\t{bld_id} /* {fname} in {phase} */ = {{isa = PBXBuildFile; fileRef = {fref_id} /* {fname} */; }};\n"
    pbx = pbx.replace("/* Begin PBXBuildFile section */\n", "/* Begin PBXBuildFile section */\n" + bld_entry)

    # PBXFileReference
    ftype = "text.json" if fname.endswith(".json") else "sourcecode.swift"
    fref_entry = f"\t\t{fref_id} /* {fname} */ = {{isa = PBXFileReference; lastKnownFileType = {ftype}; path = {fname}; sourceTree = \"<group>\"; }};\n"
    pbx = pbx.replace("/* Begin PBXFileReference section */\n", "/* Begin PBXFileReference section */\n" + fref_entry)

    # Add to group
    # We can add next to scenarios.json for Resources, or next to ScenarioDetailView for Views
    anchor = "scenarios.json */," if is_res else "TokyoVoiceBankService.swift */,"
    pbx = pbx.replace(anchor, f"{anchor}\n\t\t\t\t{fref_id} /* {fname} */,")

    # Add to Build Phase
    build_phase_anchor = "scenarios.json in Resources */," if is_res else "TokyoVoiceBankService.swift in Sources */,"
    pbx = pbx.replace(build_phase_anchor, f"{build_phase_anchor}\n\t\t\t\t{bld_id} /* {fname} in {phase} */,")

    print(f"✅ Added {fname} to project.pbxproj")

open(pbx_path, "w", encoding="utf-8").write(pbx)
print("Project pbxproj updated successfully.")
