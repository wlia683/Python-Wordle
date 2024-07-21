def combine_and_sort_wordlist(self, file1, file2, output):
        try:

            with open(file1, 'r') as file1:
                content1 = file1.readlines()

            with open(file2, 'r') as file2:
                content2 = file2.readlines()

            combined = sorted(content1 + content2)

            with open(output, 'w') as output_file:
                output_file.writelines(combined)
            
            print(f"Files combined and sorted successfully.")

        except Exception as e:
            print(f"Error: {e}")
