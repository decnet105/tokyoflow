import os
import glob
import re
import hashlib

def gen_id(seed: str) -> str:
    h = hashlib.md5(seed.encode("utf-8")).hexdigest()[:24].upper()
    return h

def main():
    pbx_path = "TokyoFlow.xcodeproj/project.pbxproj"
    with open(pbx_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find VoiceBank group ID
    group_match = re.search(r"([0-9A-F]{24})\s*/\*\s*VoiceBank\s*\*/\s*=\s*\{[^}]+children\s*=\s*\(([^)]+)\)", content)
    if not group_match:
        print("❌ Could not find VoiceBank group in pbxproj")
        return

    group_id = group_match.group(1)
    existing_group_children = group_match.group(2)

    # Find Resources phase
    res_match = re.search(r"([0-9A-F]{24})\s*/\*\s*Resources\s*\*/\s*=\s*\{[^}]+isa\s*=\s*PBXResourcesBuildPhase;[^}]+files\s*=\s*\(([^)]+)\)", content)
    if not res_match:
        print("❌ Could not find Resources phase in pbxproj")
        return

    res_id = res_match.group(1)
    existing_res_files = res_match.group(2)

    # Scan all .m4a and .json in VoiceBank
    voicebank_files = glob.glob("TokyoFlow/Resources/Audio/VoiceBank/*")
    all_files = [os.path.basename(p) for p in voicebank_files if os.path.isfile(p)]
    print(f"📁 Total files found in VoiceBank folder: {len(all_files)}")

    # Extract already referenced files
    existing_refs = set(re.findall(r'/\*\s*([^\*]+)\s*\*/', existing_group_children))
    existing_refs.update(re.findall(r'/\*\s*([^\*]+)\s+in\s+Resources\s*\*/', existing_res_files))

    files_to_add = [f for f in all_files if f not in existing_refs]
    print(f"➕ Files to add to Xcode project: {len(files_to_add)}")

    if not files_to_add:
        print("✅ All files already synced in Xcode project!")
        return

    # Generate PBXBuildFile entries, PBXFileReference entries, Group children, Resources files
    pbx_build_files = []
    pbx_file_refs = []
    group_children_entries = []
    res_phase_entries = []

    for fn in files_to_add:
        file_id = gen_id(f"fileref_{fn}")
        build_id = gen_id(f"buildfile_{fn}")
        file_type = "text.json" if fn.endswith(".json") else "audio.m4a"

        pbx_build_files.append(f"\t\t{build_id} /* {fn} in Resources */ = {{isa = PBXBuildFile; fileRef = {file_id} /* {fn} */; }};\n")
        pbx_file_refs.append(f"\t\t{file_id} /* {fn} */ = {{isa = PBXFileReference; lastKnownFileType = {file_type}; path = \"{fn}\"; sourceTree = \"<group>\"; }};\n")
        group_children_entries.append(f"\t\t\t\t{file_id} /* {fn} */,\n")
        res_phase_entries.append(f"\t\t\t\t{build_id} /* {fn} in Resources */,\n")

    # Insert into PBXBuildFile section
    build_file_section_pos = content.find("/* Begin PBXBuildFile section */")
    if build_file_section_pos != -1:
        insert_pos = content.find("\n", build_file_section_pos) + 1
        content = content[:insert_pos] + "".join(pbx_build_files) + content[insert_pos:]

    # Insert into PBXFileReference section
    file_ref_section_pos = content.find("/* Begin PBXFileReference section */")
    if file_ref_section_pos != -1:
        insert_pos = content.find("\n", file_ref_section_pos) + 1
        content = content[:insert_pos] + "".join(pbx_file_refs) + content[insert_pos:]

    # Insert into VoiceBank group children
    group_pattern = f"({group_id}\\s*/\\*\\s*VoiceBank\\s*\\*/\\s*=\\s*\\{{[^}}]+children\\s*=\\s*\\()"
    content = re.sub(group_pattern, r"\1\n" + "".join(group_children_entries), content, count=1)

    # Insert into Resources phase files
    res_pattern = f"({res_id}\\s*/\\*\\s*Resources\\s*\\*/\\s*=\\s*\\{{[^}}]+files\\s*=\\s*\\()"
    content = re.sub(res_pattern, r"\1\n" + "".join(res_phase_entries), content, count=1)

    with open(pbx_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🎉 Successfully registered {len(files_to_add)} files directly into {pbx_path}!")

if __name__ == "__main__":
    main()
