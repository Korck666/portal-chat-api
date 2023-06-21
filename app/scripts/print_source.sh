#!/bin/bash

# Print the directory structure
# echo "# Directory Structure"
# echo ""
# echo "\`\`\`text"
# tree
# echo "\`\`\`"
# echo ""
echo "\`\`\`python"
# Print the content of Python files
for file in $(find . -name "*.py")
do
  echo "# Content of $file:"
  cat $file
  echo
done
echo "\`\`\`"
