import re

pbx_path = "TokyoFlow.xcodeproj/project.pbxproj"
pbx = open(pbx_path, "r", encoding="utf-8").read()

file_ref_id = "A3B4C5D6E7F8091A2B3C4D5E"
build_file_id = "B4C5D6E7F8091A2B3C4D5E6F"

if file_ref_id not in pbx:
    # 1. PBXBuildFile
    build_entry = f"\t\t{build_file_id} /* NotificationService.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {file_ref_id} /* NotificationService.swift */; }};\n"
    pbx = pbx.replace("/* Begin PBXBuildFile section */\n", "/* Begin PBXBuildFile section */\n" + build_entry)

    # 2. PBXFileReference
    file_ref_entry = f"\t\t{file_ref_id} /* NotificationService.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = NotificationService.swift; sourceTree = \"<group>\"; }};\n"
    pbx = pbx.replace("/* Begin PBXFileReference section */\n", "/* Begin PBXFileReference section */\n" + file_ref_entry)

    # 3. Add to Services PBXGroup
    # Find TokyoVoiceBankService.swift in group and add NotificationService right next to it
    pbx = pbx.replace(
        "A1B2C3D4E5F60718293A4B5C /* TokyoVoiceBankService.swift */,",
        f"A1B2C3D4E5F60718293A4B5C /* TokyoVoiceBankService.swift */,\n\t\t\t\t{file_ref_id} /* NotificationService.swift */,"
    )

    # 4. Add to PBXSourcesBuildPhase
    pbx = pbx.replace(
        "B2C3D4E5F60718293A4B5C6D /* TokyoVoiceBankService.swift in Sources */,",
        f"B2C3D4E5F60718293A4B5C6D /* TokyoVoiceBankService.swift in Sources */,\n\t\t\t\t{build_file_id} /* NotificationService.swift in Sources */,"
    )

    open(pbx_path, "w", encoding="utf-8").write(pbx)
    print("✅ Added NotificationService.swift to project.pbxproj")
else:
    print("NotificationService.swift already in project.pbxproj")
