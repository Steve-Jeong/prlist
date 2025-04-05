#!/usr/bin/env python3
"""
prlist - 디렉토리 내 파일들을 하나로 병합하는 도구

이 스크립트는 지정된 디렉토리 내의 모든 파일을 읽어 하나의 출력으로 결합합니다.
각 파일 내용 앞에는 해당 파일의 경로가 주석으로 추가됩니다.
.prlistignore 파일을 사용하여 특정 파일이나 디렉토리를 처리에서 제외할 수 있습니다.

사용법: prlist <directory>
"""
import os
import sys
import fnmatch

def read_ignore_patterns(directory):
    """
    .prlistignore 파일에서 무시할 패턴을 읽어옵니다.
    """
    ignore_file = os.path.join(directory, '.prlistignore')
    ignore_patterns = []

    if os.path.exists(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)

    return ignore_patterns

def should_ignore(path, ignore_patterns):
    """
    주어진 경로가 무시할 패턴에 해당하는지 확인합니다.
    """
    path_parts = path.split(os.sep)
    for pattern in ignore_patterns:
        for part in path_parts:
            if fnmatch.fnmatch(part, pattern):
                return True
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def collect_files(directory, ignore_patterns):
    """
    디렉토리에서 파일을 수집합니다. 무시할 패턴에 해당하는 파일은 제외합니다.
    """
    files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, directory)

            if should_ignore(rel_path, ignore_patterns):
                continue

            files.append(rel_path)

    return sorted(files)  # 정렬된 파일 목록 반환

def combine_files(directory, files):
    """
    파일들의 내용을 하나로 합치고 각 파일 앞에 경로 정보를 추가합니다.
    """
    combined_content = []

    for file in files:
        # 파일 경로 생성
        file_path = os.path.join(directory, file)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 디렉토리 이름 앞에 './'를 붙임
            if directory != '.':  # 현재 디렉토리가 아닌 경우에만 접두사 추가
                header = (f"//#########################################################\n"
                          f"//\n"
                          f"// ./{os.path.basename(directory)}/{file}\n"  # 디렉토리 이름 앞에 './' 추가
                          f"//\n"
                          f"//*********************************************************\n"
                          )
            else: # 현재 디렉토리인경우에는 파일이름만 추가
                header = (f"//#########################################################\n"
                          f"//\n"
                          f"// {file}\n"
                          f"//\n"
                          f"//*********************************************************\n"
                          )

            combined_content.append(header + content + "\n\n")

        except FileNotFoundError:
            combined_content.append(f"// {file}\n// Error: File not found\n\n")
        except PermissionError:
            combined_content.append(f"// {file}\n// Error: Permission denied\n\n")
        except IsADirectoryError:
            combined_content.append(f"// {file}\n// Error: Is a directory\n\n")
        except UnicodeDecodeError:
            combined_content.append(f"// {file}\n// Error: Cannot decode file (binary file?)\n\n")
        except IOError as e:
            combined_content.append(f"// {file}\n// Error reading file: {str(e)}\n\n")

    return "".join(combined_content)

def main():
    """
    메인 함수: 명령줄 인수를 처리하고 디렉토리 내 파일들을 병합합니다.

    명령줄에서 디렉토리 경로를 받아 해당 디렉토리의 모든 파일을 읽고,
    .prlistignore에 명시된 패턴에 해당하는 파일을 제외한 모든 파일의 내용을
    하나로 합쳐 출력합니다.
    """
    if len(sys.argv) != 2:
        print("Usage: prlist <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    # 무시할 패턴 읽기
    ignore_patterns = read_ignore_patterns(directory)

    # ignore_patterns 출력
    print("Ignoring patterns:")
    if ignore_patterns:
        for pattern in ignore_patterns:
            print(f"  - {pattern}")
    else:
        print("  None (no .prlistignore file found or file is empty)")
    print()

    # 파일 수집
    files = collect_files(directory, ignore_patterns)

    if not files:
        print(f"No files found in '{directory}' (or all files are ignored)")
        sys.exit(0)

    # 파일 내용 합치기
    combined_content = combine_files(directory, files)

    # 결과 출력
    print(combined_content)

if __name__ == "__main__":
    main()
