"""
Problem Generator - Batch 3: Strings (6 problems) + Stack and Queue (6 problems)
Strings mix: 3 Easy, 2 Medium, 1 Hard
Stack and Queue mix: 3 Easy, 2 Medium, 1 Hard
"""
import os
import json

PROBLEMS = [
    # 19. Strings - Easy
    {
        "slug": "valid-palindrome-with-single-removal",
        "title": "Valid Palindrome with Single Character Removal",
        "difficulty": "easy",
        "topic": "Strings",
        "tags": ["Two Pointers", "String", "Greedy"],
        "company_tags": ["Meta", "Amazon", "Microsoft"],
        "statement_md": "Given a string `s`, return `true` if the `s` can be a palindrome after deleting at most one character from it.\n\n### Input Format\n- A string `s`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "\"aba\"",
                "output": "true",
                "explanation": "\"aba\" is already a palindrome."
            },
            {
                "input": "\"abca\"",
                "output": "true",
                "explanation": "You could delete the character 'c' to get \"aba\"."
            }
        ],
        "sample_tests": [
            {"input_text": "\"aba\"", "expected_output": "true"},
            {"input_text": "\"abca\"", "expected_output": "true"},
            {"input_text": "\"abc\"", "expected_output": "false"}
        ],
        "hidden_tests": [
            {"input_text": "\"a\"", "expected_output": "true"},
            {"input_text": "\"ab\"", "expected_output": "true"},
            {"input_text": "\"deeee\"", "expected_output": "true"},
            {"input_text": "\"eeeed\"", "expected_output": "true"},
            {"input_text": "\"aguokpatgbnvfqmgmlcupuufxoohdfpgjdmysgvhmvffcnqxjjxqncffvmhvgsymdjgpfdhooxfuupuculmgmqfvnbgtapkouga\"", "expected_output": "true"},
            {"input_text": "\"raceecar\"", "expected_output": "true"},
            {"input_text": "\"abccbda\"", "expected_output": "true"},
            {"input_text": "\"abcdefba\"", "expected_output": "false"},
            {"input_text": "\"bddb\"", "expected_output": "true"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Start two pointers from the outer ends converging inward.", "xp_cost": 2},
            {"level": 2, "text": "Upon the first mismatch at s[left] != s[right], check whether deleting s[left] or s[right] produces a valid palindrome.", "xp_cost": 5},
            {"level": 3, "text": "Use Two Pointers with a helper function to verify standard palindrome subsegments.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Two Pointers Branching\n\nIterate with `left = 0`, `right = len(s) - 1`. If `s[left] == s[right]`, advance both. When a mismatch is encountered, check if either `s[left+1:right+1]` or `s[left:right]` is a palindrome. If neither, return false.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass with at most one branching check.\n- **Space Complexity:** $O(1)$ constant auxiliary memory.\n\n#### Common Pitfalls\n- Trying to delete from both sides instead of checking the two alternate branches.",
        "reference_solutions": {
            "brute_python": "def validPalindrome(s):\n    if s == s[::-1]: return True\n    for i in range(len(s)):\n        cand = s[:i] + s[i+1:]\n        if cand == cand[::-1]: return True\n    return False",
            "optimal_python": "def validPalindrome(s):\n    def is_pal(sub, l, r):\n        while l < r:\n            if sub[l] != sub[r]: return False\n            l += 1\n            r -= 1\n        return True\n    left, right = 0, len(s) - 1\n    while left < right:\n        if s[left] != s[right]:\n            return is_pal(s, left + 1, right) or is_pal(s, left, right - 1)\n        left += 1\n        right -= 1\n    return True",
            "optimal_java": "public class Solution {\n    public boolean validPalindrome(String s) {\n        int left = 0, right = s.length() - 1;\n        while (left < right) {\n            if (s.charAt(left) != s.charAt(right)) {\n                return isPal(s, left + 1, right) || isPal(s, left, right - 1);\n            }\n            left++;\n            right--;\n        }\n        return true;\n    }\n    private boolean isPal(String s, int l, int r) {\n        while (l < r) {\n            if (s.charAt(l) != s.charAt(r)) return false;\n            l++;\n            r--;\n        }\n        return true;\n    }\n}",
            "optimal_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool isPal(const string& s, int l, int r) {\n        while (l < r) {\n            if (s[l] != s[r]) return false;\n            l++;\n            r--;\n        }\n        return true;\n    }\n    bool validPalindrome(string s) {\n        int left = 0, right = (int)s.size() - 1;\n        while (left < right) {\n            if (s[left] != s[right]) {\n                return isPal(s, left + 1, right) || isPal(s, left, right - 1);\n            }\n            left++;\n            right--;\n        }\n        return true;\n    }\n};"
        }
    },

    # 20. Strings - Easy
    {
        "slug": "string-compression-run-lengths",
        "title": "String Compression by Run Lengths",
        "difficulty": "easy",
        "topic": "Strings",
        "tags": ["Two Pointers", "String"],
        "company_tags": ["Amazon", "Microsoft", "Bloomberg"],
        "statement_md": "Given an array of characters `chars`, compress it in-place using the following algorithm:\n\nBegin with an empty string `s`. For each group of consecutive repeating characters in `chars`:\n- If the group's length is 1, append the character to `s`.\n- Otherwise, append the character followed by the group's length.\n\nThe compressed string `s` should not be returned separately, but instead, be stored in the input character array `chars`.\n\nReturn the new length of the array.\n\n### Input Format\n- A JSON-encoded list of single-character strings `chars`\n\n### Output Format\n- An integer representing the compressed length",
        "examples": [
            {
                "input": "[\"a\", \"a\", \"b\", \"b\", \"c\", \"c\", \"c\"]",
                "output": "6",
                "explanation": "The groups are \"aa\", \"bb\", and \"ccc\". This compresses to \"a2b2c3\", which has length 6."
            },
            {
                "input": "[\"a\"]",
                "output": "1",
                "explanation": "Single character \"a\" is uncompressed, length 1."
            }
        ],
        "sample_tests": [
            {"input_text": "[\"a\", \"a\", \"b\", \"b\", \"c\", \"c\", \"c\"]", "expected_output": "6"},
            {"input_text": "[\"a\"]", "expected_output": "1"},
            {"input_text": "[\"a\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\", \"b\"]", "expected_output": "4"}
        ],
        "hidden_tests": [
            {"input_text": "[\"a\", \"b\", \"c\"]", "expected_output": "3"},
            {"input_text": "[\"a\", \"a\"]", "expected_output": "2"},
            {"input_text": "[\"z\", \"z\", \"z\", \"z\", \"z\"]", "expected_output": "2"},
            {"input_text": "[\"o\", \"o\", \"o\", \"p\", \"q\", \"q\"]", "expected_output": "5"},
            {"input_text": "[\"a\", \"a\", \"a\", \"a\", \"a\", \"a\", \"a\", \"a\", \"a\", \"a\"]", "expected_output": "3"},
            {"input_text": "[\"x\", \"y\", \"y\", \"z\", \"z\", \"z\"]", "expected_output": "5"},
            {"input_text": "[\"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\", \"m\"]", "expected_output": "3"},
            {"input_text": "[\"p\", \"p\", \"p\", \"p\"]", "expected_output": "2"},
            {"input_text": "[\"k\", \"k\", \"r\", \"r\", \"r\", \"s\"]", "expected_output": "5"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Group consecutive identical characters using a read pointer.", "xp_cost": 2},
            {"level": 2, "text": "Write the character to the write pointer, and if the count is greater than 1, write each digit of the count.", "xp_cost": 5},
            {"level": 3, "text": "Use Fast and Slow Pointers to achieve in-place constant space rewriting.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: In-Place Two Pointers\n\nMaintain `write = 0` and `read = 0`. For each run of identical characters starting at `read`, count occurrences until character changes at `read_end`. Write character at `chars[write]`. If count > 1, write string representation of count digit by digit.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ in-place modification.\n\n#### Common Pitfalls\n- Multidigit counts (e.g. 12 -> '1', '2') must occupy separate array cells.",
        "reference_solutions": {
            "brute_python": "def compress(chars):\n    res = []\n    i = 0\n    while i < len(chars):\n        ch = chars[i]\n        count = 0\n        while i < len(chars) and chars[i] == ch:\n            count += 1\n            i += 1\n        res.append(ch)\n        if count > 1:\n            res.extend(list(str(count)))\n    for j in range(len(res)): chars[j] = res[j]\n    return len(res)",
            "optimal_python": "def compress(chars):\n    write = 0\n    read = 0\n    n = len(chars)\n    while read < n:\n        ch = chars[read]\n        count = 0\n        while read < n and chars[read] == ch:\n            count += 1\n            read += 1\n        chars[write] = ch\n        write += 1\n        if count > 1:\n            for digit in str(count):\n                chars[write] = digit\n                write += 1\n    return write",
            "optimal_java": "public class Solution {\n    public int compress(char[] chars) {\n        int write = 0, read = 0, n = chars.length;\n        while (read < n) {\n            char ch = chars[read];\n            int count = 0;\n            while (read < n && chars[read] == ch) {\n                count++;\n                read++;\n            }\n            chars[write++] = ch;\n            if (count > 1) {\n                for (char c : Integer.toString(count).toCharArray()) {\n                    chars[write++] = c;\n                }\n            }\n        }\n        return write;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int compress(vector<char>& chars) {\n        int write = 0, read = 0, n = chars.size();\n        while (read < n) {\n            char ch = chars[read];\n            int count = 0;\n            while (read < n && chars[read] == ch) {\n                count++;\n                read++;\n            }\n            chars[write++] = ch;\n            if (count > 1) {\n                for (char c : to_string(count)) {\n                    chars[write++] = c;\n                }\n            }\n        }\n        return write;\n    }\n};"
        }
    },

    # 21. Strings - Easy
    {
        "slug": "isomorphic-code-cipher",
        "title": "Isomorphic Character Cipher Validation",
        "difficulty": "easy",
        "topic": "Strings",
        "tags": ["Hash Table", "String"],
        "company_tags": ["LinkedIn", "Amazon", "Google"],
        "statement_md": "Given two strings `s` and `t`, determine if they are isomorphic.\n\nTwo strings `s` and `t` are isomorphic if the characters in `s` can be replaced to get `t`.\n\nAll occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.\n\n### Input Format\n- Line 1: String `s`\n- Line 2: String `t`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "\"egg\"\n\"add\"",
                "output": "true",
                "explanation": "'e' maps to 'a', and 'g' maps to 'd'."
            },
            {
                "input": "\"foo\"\n\"bar\"",
                "output": "false",
                "explanation": "'o' maps to both 'a' and 'r', which is invalid."
            }
        ],
        "sample_tests": [
            {"input_text": "\"egg\"\n\"add\"", "expected_output": "true"},
            {"input_text": "\"foo\"\n\"bar\"", "expected_output": "false"},
            {"input_text": "\"paper\"\n\"title\"", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"\n\"\"", "expected_output": "true"},
            {"input_text": "\"a\"\n\"b\"", "expected_output": "true"},
            {"input_text": "\"ab\"\n\"aa\"", "expected_output": "false"},
            {"input_text": "\"badc\"\n\"baba\"", "expected_output": "false"},
            {"input_text": "\"bbbaaaba\"\n\"aaabbbba\"", "expected_output": "false"},
            {"input_text": "\"abcdefg\"\n\"1234567\"", "expected_output": "true"},
            {"input_text": "\"abcde\"\n\"vwxyz\"", "expected_output": "true"},
            {"input_text": "\"13\"\n\"42\"", "expected_output": "true"},
            {"input_text": "\"aa\"\n\"ab\"", "expected_output": "false"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "A valid bijection requires mapping s -> t AND t -> s simultaneously.", "xp_cost": 2},
            {"level": 2, "text": "Maintain two maps: one from s to t and one from t to s.", "xp_cost": 5},
            {"level": 3, "text": "Use Dual Hash Maps or Character Arrays to ensure a strict one-to-one correspondence.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Dual Hash Maps\n\nTo ensure a bijective mapping, maintain `s_to_t` and `t_to_s`. At each position `i`, check that `s_to_t[s[i]] == t[i]` and `t_to_s[t[i]] == s[i]`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(1)$ alphabet size bound (at most 256 characters).\n\n#### Common Pitfalls\n- Checking only one direction (e.g. `\"ab\"` and `\"aa\"` where 'a' maps to 'a' and 'b' maps to 'a').",
        "reference_solutions": {
            "brute_python": "def isIsomorphic(s, t):\n    return len(set(zip(s, t))) == len(set(s)) == len(set(t))",
            "optimal_python": "def isIsomorphic(s, t):\n    if len(s) != len(t): return False\n    s_to_t, t_to_s = {}, {}\n    for c1, c2 in zip(s, t):\n        if (c1 in s_to_t and s_to_t[c1] != c2) or (c2 in t_to_s and t_to_s[c2] != c1):\n            return False\n        s_to_t[c1] = c2\n        t_to_s[c2] = c1\n    return True",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public boolean isIsomorphic(String s, String t) {\n        if (s.length() != t.length()) return false;\n        Map<Character, Character> m1 = new HashMap<>(), m2 = new HashMap<>();\n        for (int i = 0; i < s.length(); i++) {\n            char c1 = s.charAt(i), c2 = t.charAt(i);\n            if (m1.containsKey(c1) && m1.get(c1) != c2) return false;\n            if (m2.containsKey(c2) && m2.get(c2) != c1) return false;\n            m1.put(c1, c2);\n            m2.put(c2, c1);\n        }\n        return true;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    bool isIsomorphic(string s, string t) {\n        if (s.size() != t.size()) return false;\n        unordered_map<char, char> m1, m2;\n        for (int i = 0; i < (int)s.size(); i++) {\n            char c1 = s[i], c2 = t[i];\n            if (m1.count(c1) && m1[c1] != c2) return false;\n            if (m2.count(c2) && m2[c2] != c1) return false;\n            m1[c1] = c2;\n            m2[c2] = c1;\n        }\n        return true;\n    }\n};"
        }
    },

    # 22. Strings - Medium
    {
        "slug": "repeated-dna-sequence-signatures",
        "title": "Repeated DNA 10-mer Sequence Signatures",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Hash Table", "String", "Bit Manipulation", "Rolling Hash"],
        "company_tags": ["LinkedIn", "Amazon", "Google"],
        "statement_md": "The DNA sequence is composed of a series of nucleotides abbreviated as `'A'`, `'C'`, `'G'`, and `'T'`.\n\nWhen studying DNA, it is useful to identify repeated sequences within the DNA.\n\nGiven a string `s` that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. You may return the answer in sorted order.\n\n### Input Format\n- A string `s`\n\n### Output Format\n- A JSON-encoded list of sorted 10-character strings",
        "examples": [
            {
                "input": "\"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT\"",
                "output": "[\"AAAAACCCCC\", \"CCCCCAAAAA\"]",
                "explanation": "\"AAAAACCCCC\" and \"CCCCCAAAAA\" both appear multiple times."
            },
            {
                "input": "\"AAAAAAAAAAAAA\"",
                "output": "[\"AAAAAAAAAA\"]",
                "explanation": "\"AAAAAAAAAA\" appears 4 times at different offsets."
            }
        ],
        "sample_tests": [
            {"input_text": "\"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT\"", "expected_output": "[\"AAAAACCCCC\", \"CCCCCAAAAA\"]"},
            {"input_text": "\"AAAAAAAAAAAAA\"", "expected_output": "[\"AAAAAAAAAA\"]"},
            {"input_text": "\"ACGTACGTAC\"", "expected_output": "[]"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"", "expected_output": "[]"},
            {"input_text": "\"AAAAAAAAAA\"", "expected_output": "[]"},
            {"input_text": "\"AAAAAAAAAAA\"", "expected_output": "[\"AAAAAAAAAA\"]"},
            {"input_text": "\"ACGTACGTACACGTACGTAC\"", "expected_output": "[\"ACGTACGTAC\"]"},
            {"input_text": "\"CCCCCCCCCCCCCCCCCCCC\"", "expected_output": "[\"CCCCCCCCCC\"]"},
            {"input_text": "\"AGCTAGCTAGAGCTAGCTAG\"", "expected_output": "[\"AGCTAGCTAG\"]"},
            {"input_text": "\"TATATATATATATATATATATATA\"", "expected_output": "[\"ATATATATAT\", \"TATATATATA\"]"},
            {"input_text": "\"GCATGCATGCGCATGCATGC\"", "expected_output": "[\"GCATGCATGC\"]"},
            {"input_text": "\"GATCGATCGATCGATCGATCGATC\"", "expected_output": "[\"ATCGATCGAT\", \"CGATCGATCG\", \"GATCGATCGA\", \"TCGATCGATC\"]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Extract all windows of length 10 as you traverse s from left to right.", "xp_cost": 2},
            {"level": 2, "text": "Maintain two sets: 'seen' for patterns observed once, and 'repeated' for patterns observed >= 2 times.", "xp_cost": 5},
            {"level": 3, "text": "Use a Hash Set or 2-bit Rolling Hash for O(1) sequence signatures.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Rolling Hash Set\n\nIterate through all substrings of length 10. Track seen sequences in `seen`. If a sequence is already in `seen`, add it to `repeated`. Return sorted list.\n\n#### Complexity\n- **Time Complexity:** $O((n - 10) \\cdot 10) = O(n)$ time.\n- **Space Complexity:** $O(n)$ space for hash set.\n\n#### Common Pitfalls\n- Returning duplicates in the output list (avoided by using a set for repeated entries).",
        "reference_solutions": {
            "brute_python": "def findRepeatedDnaSequences(s):\n    seen = set()\n    repeated = set()\n    for i in range(len(s) - 9):\n        sub = s[i:i+10]\n        if sub in seen:\n            repeated.add(sub)\n        seen.add(sub)\n    return sorted(list(repeated))",
            "optimal_python": "def findRepeatedDnaSequences(s):\n    seen = set()\n    repeated = set()\n    for i in range(len(s) - 9):\n        sub = s[i:i+10]\n        if sub in seen:\n            repeated.add(sub)\n        else:\n            seen.add(sub)\n    return sorted(list(repeated))",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<String> findRepeatedDnaSequences(String s) {\n        Set<String> seen = new HashSet<>(), repeated = new HashSet<>();\n        for (int i = 0; i + 9 < s.length(); i++) {\n            String sub = s.substring(i, i + 10);\n            if (seen.contains(sub)) repeated.add(sub);\n            else seen.add(sub);\n        }\n        List<String> res = new ArrayList<>(repeated);\n        Collections.sort(res);\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <string>\n#include <unordered_set>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> findRepeatedDnaSequences(string s) {\n        unordered_set<string> seen, repeated;\n        for (int i = 0; i + 9 < (int)s.size(); i++) {\n            string sub = s.substr(i, 10);\n            if (seen.count(sub)) repeated.insert(sub);\n            else seen.insert(sub);\n        }\n        vector<string> res(repeated.begin(), repeated.end());\n        sort(res.begin(), res.end());\n        return res;\n    }\n};"
        }
    },

    # 23. Strings - Medium
    {
        "slug": "string-multiplication-without-builtins",
        "title": "String Multiplication Without Built-In BigInt",
        "difficulty": "medium",
        "topic": "Strings",
        "tags": ["Math", "String", "Simulation"],
        "company_tags": ["Meta", "Amazon", "Microsoft"],
        "statement_md": "Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.\n\nNote: You must not use any built-in BigInteger library or convert the inputs to integer directly.\n\n### Input Format\n- Line 1: String `num1`\n- Line 2: String `num2`\n\n### Output Format\n- A string representing the product",
        "examples": [
            {
                "input": "\"2\"\n\"3\"",
                "output": "\"6\"",
                "explanation": "2 * 3 = 6."
            },
            {
                "input": "\"123\"\n\"456\"",
                "output": "\"56088\"",
                "explanation": "123 * 456 = 56088."
            }
        ],
        "sample_tests": [
            {"input_text": "\"2\"\n\"3\"", "expected_output": "\"6\""},
            {"input_text": "\"123\"\n\"456\"", "expected_output": "\"56088\""},
            {"input_text": "\"0\"\n\"52\"", "expected_output": "\"0\""}
        ],
        "hidden_tests": [
            {"input_text": "\"0\"\n\"0\"", "expected_output": "\"0\""},
            {"input_text": "\"1\"\n\"1\"", "expected_output": "\"1\""},
            {"input_text": "\"9\"\n\"9\"", "expected_output": "\"81\""},
            {"input_text": "\"99\"\n\"99\"", "expected_output": "\"9801\""},
            {"input_text": "\"1000\"\n\"1000\"", "expected_output": "\"1000000\""},
            {"input_text": "\"98765\"\n\"4321\"", "expected_output": "\"426763565\""},
            {"input_text": "\"123456789\"\n\"987654321\"", "expected_output": "\"121932631112635269\""},
            {"input_text": "\"99999\"\n\"0\"", "expected_output": "\"0\""},
            {"input_text": "\"25\"\n\"25\"", "expected_output": "\"625\""}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that multiplying num1[i] and num2[j] places digits at indices i + j and i + j + 1 in a result array of size len(num1) + len(num2).", "xp_cost": 2},
            {"level": 2, "text": "Work from right to left like grade-school column multiplication.", "xp_cost": 5},
            {"level": 3, "text": "Use an Array of size m + n to accumulate partial products and carry digits.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Column Multiplication Simulation\n\nAllocate an integer array `res` of size `len(num1) + len(num2)`. Multiply each digit `num1[i] * num2[j]`. Add to `res[i + j + 1]`, carry to `res[i + j]`. Strip leading zeros and format as string.\n\n#### Complexity\n- **Time Complexity:** $O(m \\cdot n)$ where $m$ and $n$ are string lengths.\n- **Space Complexity:** $O(m + n)$ for output digit array.\n\n#### Common Pitfalls\n- Multiplying by \"0\" must return \"0\", not \"0000\".",
        "reference_solutions": {
            "brute_python": "def multiply(num1, num2):\n    if num1 == '0' or num2 == '0': return '0'\n    res = [0] * (len(num1) + len(num2))\n    for i in range(len(num1) - 1, -1, -1):\n        for j in range(len(num2) - 1, -1, -1):\n            mul = int(num1[i]) * int(num2[j])\n            p1, p2 = i + j, i + j + 1\n            total = mul + res[p2]\n            res[p2] = total % 10\n            res[p1] += total // 10\n    s = ''.join(map(str, res)).lstrip('0')\n    return s if s else '0'",
            "optimal_python": "def multiply(num1, num2):\n    if num1 == '0' or num2 == '0':\n        return '0'\n    m, n = len(num1), len(num2)\n    res = [0] * (m + n)\n    for i in range(m - 1, -1, -1):\n        d1 = ord(num1[i]) - ord('0')\n        for j in range(n - 1, -1, -1):\n            d2 = ord(num2[j]) - ord('0')\n            total = d1 * d2 + res[i + j + 1]\n            res[i + j + 1] = total % 10\n            res[i + j] += total // 10\n    idx = 0\n    while idx < len(res) and res[idx] == 0:\n        idx += 1\n    return ''.join(map(str, res[idx:]))",
            "optimal_java": "public class Solution {\n    public String multiply(String num1, String num2) {\n        if (\"0\".equals(num1) || \"0\".equals(num2)) return \"0\";\n        int m = num1.length(), n = num2.length();\n        int[] pos = new int[m + n];\n        for (int i = m - 1; i >= 0; i--) {\n            for (int j = n - 1; j >= 0; j--) {\n                int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');\n                int p1 = i + j, p2 = i + j + 1;\n                int sum = mul + pos[p2];\n                pos[p1] += sum / 10;\n                pos[p2] = sum % 10;\n            }\n        }\n        StringBuilder sb = new StringBuilder();\n        for (int p : pos) if (!(sb.length() == 0 && p == 0)) sb.append(p);\n        return sb.length() == 0 ? \"0\" : sb.toString();\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    string multiply(string num1, string num2) {\n        if (num1 == \"0\" || num2 == \"0\") return \"0\";\n        int m = num1.size(), n = num2.size();\n        vector<int> res(m + n, 0);\n        for (int i = m - 1; i >= 0; i--) {\n            for (int j = n - 1; j >= 0; j--) {\n                int mul = (num1[i] - '0') * (num2[j] - '0');\n                int p1 = i + j, p2 = i + j + 1;\n                int total = mul + res[p2];\n                res[p2] = total % 10;\n                res[p1] += total / 10;\n            }\n        }\n        string s = \"\";\n        for (int num : res) {\n            if (!(s.empty() && num == 0)) s.push_back(num + '0');\n        }\n        return s.empty() ? \"0\" : s;\n    }\n};"
        }
    },

    # 24. Strings - Hard
    {
        "slug": "shortest-palindrome-prefix-extension",
        "title": "Shortest Palindrome via Minimum Prefix Extension",
        "difficulty": "hard",
        "topic": "Strings",
        "tags": ["String", "KMP", "Rolling Hash"],
        "company_tags": ["Google", "Amazon", "Apple"],
        "statement_md": "You are given a string `s`. You can convert `s` to a palindrome by adding characters in front of it.\n\nReturn the shortest palindrome you can find by performing this transformation.\n\n### Input Format\n- A string `s`\n\n### Output Format\n- A string representing the shortest palindrome",
        "examples": [
            {
                "input": "\"aacecaaa\"",
                "output": "\"aaacecaaa\"",
                "explanation": "Adding 'a' to the front produces the shortest palindrome."
            },
            {
                "input": "\"abcd\"",
                "output": "\"dcbabcd\"",
                "explanation": "Adding \"dcb\" to the front produces the palindrome."
            }
        ],
        "sample_tests": [
            {"input_text": "\"aacecaaa\"", "expected_output": "\"aaacecaaa\""},
            {"input_text": "\"abcd\"", "expected_output": "\"dcbabcd\""},
            {"input_text": "\"\"", "expected_output": "\"\""}
        ],
        "hidden_tests": [
            {"input_text": "\"a\"", "expected_output": "\"a\""},
            {"input_text": "\"ab\"", "expected_output": "\"bab\""},
            {"input_text": "\"aba\"", "expected_output": "\"aba\""},
            {"input_text": "\"abacaba\"", "expected_output": "\"abacaba\""},
            {"input_text": "\"racecar\"", "expected_output": "\"racecar\""},
            {"input_text": "\"abcde\"", "expected_output": "\"edcbabcde\""},
            {"input_text": "\"ba\"", "expected_output": "\"aba\""},
            {"input_text": "\"abbacd\"", "expected_output": "\"dcabbacd\""},
            {"input_text": "\"babbbabbaba\"", "expected_output": "\"ababbabbbabbaba\""}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "The problem is equivalent to finding the longest palindromic prefix of s.", "xp_cost": 2},
            {"level": 2, "text": "Consider constructing combined string s + '#' + reverse(s).", "xp_cost": 5},
            {"level": 3, "text": "Use the KMP Prefix Table (pi table) on s + '#' + reverse(s) to find the longest palindromic prefix in O(n) time.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: KMP Prefix Function\n\nForm `combined = s + '#' + s[::-1]`. Compute the KMP failure array ($\\pi$ table). The last entry `pi[-1]` corresponds to the length of the longest prefix of `s` that is also a suffix of `s[::-1]`, which is precisely the longest palindromic prefix. Prepend the reversed remaining suffix of `s`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ linear KMP preprocessing.\n- **Space Complexity:** $O(n)$ prefix table storage.\n\n#### Common Pitfalls\n- Not using a delimiter character like `'#'` between `s` and `reverse(s)`.",
        "reference_solutions": {
            "brute_python": "def shortestPalindrome(s):\n    n = len(s)\n    for i in range(n, -1, -1):\n        if s[:i] == s[:i][::-1]:\n            return s[i:][::-1] + s\n    return \"\"",
            "optimal_python": "def shortestPalindrome(s):\n    if not s: return \"\"\n    rev = s[::-1]\n    combined = s + '#' + rev\n    pi = [0] * len(combined)\n    j = 0\n    for i in range(1, len(combined)):\n        while j > 0 and combined[i] != combined[j]:\n            j = pi[j - 1]\n        if combined[i] == combined[j]:\n            j += 1\n        pi[i] = j\n    longest_pal = pi[-1]\n    return rev[:len(s) - longest_pal] + s",
            "optimal_java": "public class Solution {\n    public String shortestPalindrome(String s) {\n        if (s == null || s.length() == 0) return \"\";\n        String rev = new StringBuilder(s).reverse().toString();\n        String combined = s + \"#\" + rev;\n        int[] pi = new int[combined.length()];\n        int j = 0;\n        for (int i = 1; i < combined.length(); i++) {\n            while (j > 0 && combined.charAt(i) != combined.charAt(j)) j = pi[j - 1];\n            if (combined.charAt(i) == combined.charAt(j)) j++;\n            pi[i] = j;\n        }\n        int palLen = pi[combined.length() - 1];\n        return rev.substring(0, s.length() - palLen) + s;\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    string shortestPalindrome(string s) {\n        if (s.empty()) return \"\";\n        string rev = s;\n        reverse(rev.begin(), rev.end());\n        string combined = s + \"#\" + rev;\n        vector<int> pi(combined.size(), 0);\n        int j = 0;\n        for (int i = 1; i < (int)combined.size(); i++) {\n            while (j > 0 && combined[i] != combined[j]) j = pi[j - 1];\n            if (combined[i] == combined[j]) j++;\n            pi[i] = j;\n        }\n        int palLen = pi.back();\n        return rev.substr(0, s.size() - palLen) + s;\n    }\n};"
        }
    },

    # 25. Stack and Queue - Easy
    {
        "slug": "balanced-bracket-delimiter-validator",
        "title": "Nested Bracket Delimiter Balancing",
        "difficulty": "easy",
        "topic": "Stack and Queue",
        "tags": ["Stack", "String"],
        "company_tags": ["Meta", "Amazon", "Google", "Microsoft"],
        "statement_md": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.\n\n### Input Format\n- A string `s`\n\n### Output Format\n- A boolean value (`true` or `false`)",
        "examples": [
            {
                "input": "\"()[]{}\"",
                "output": "true",
                "explanation": "All brackets open and close in matching pairs."
            },
            {
                "input": "\"(]\"",
                "output": "false",
                "explanation": "Closing bracket ']' does not match opening '('."
            }
        ],
        "sample_tests": [
            {"input_text": "\"()[]{}\"", "expected_output": "true"},
            {"input_text": "\"(]\"", "expected_output": "false"},
            {"input_text": "\"([])\"", "expected_output": "true"}
        ],
        "hidden_tests": [
            {"input_text": "\"\"", "expected_output": "true"},
            {"input_text": "\"(\"", "expected_output": "false"},
            {"input_text": "\")\"", "expected_output": "false"},
            {"input_text": "\"()\"", "expected_output": "true"},
            {"input_text": "\"{[]}\"", "expected_output": "true"},
            {"input_text": "\"([)]\"", "expected_output": "false"},
            {"input_text": "\"[({})]\"", "expected_output": "true"},
            {"input_text": "\"((((((()))))))\"", "expected_output": "true"},
            {"input_text": "\"))((\"", "expected_output": "false"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Push opening brackets onto a collection and pop matching pairs when closing brackets arrive.", "xp_cost": 2},
            {"level": 2, "text": "Check if top of collection matches the closing bracket type; if empty or mismatched, return false.", "xp_cost": 5},
            {"level": 3, "text": "Use a LIFO Stack to match innermost brackets first.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: LIFO Stack Matching\n\nIterate through string characters. Push open brackets onto stack. For closing brackets, check if stack is non-empty and top element matches. Finally, ensure stack is empty.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass.\n- **Space Complexity:** $O(n)$ stack storage.\n\n#### Common Pitfalls\n- Returning true when stack still contains unclosed opening brackets.",
        "reference_solutions": {
            "brute_python": "def isValid(s):\n    while '()' in s or '[]' in s or '{}' in s:\n        s = s.replace('()', '').replace('[]', '').replace('{}', '')\n    return s == ''",
            "optimal_python": "def isValid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for c in s:\n        if c in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[c] != top:\n                return False\n        else:\n            stack.append(c)\n    return len(stack) == 0",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public boolean isValid(String s) {\n        Stack<Character> stack = new Stack<>();\n        for (char c : s.toCharArray()) {\n            if (c == '(') stack.push(')');\n            else if (c == '{') stack.push('}');\n            else if (c == '[') stack.push(']');\n            else if (stack.isEmpty() || stack.pop() != c) return false;\n        }\n        return stack.isEmpty();\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <stack>\nusing namespace std;\nclass Solution {\npublic:\n    bool isValid(string s) {\n        stack<char> st;\n        for (char c : s) {\n            if (c == '(') st.push(')');\n            else if (c == '{') st.push('}');\n            else if (c == '[') st.push(']');\n            else {\n                if (st.empty() || st.top() != c) return false;\n                st.pop();\n            }\n        }\n        return st.empty();\n    }\n};"
        }
    },

    # 26. Stack and Queue - Easy
    {
        "slug": "queue-using-dual-amortized-stacks",
        "title": "FIFO Queue Simulation Using Dual Stacks",
        "difficulty": "easy",
        "topic": "Stack and Queue",
        "tags": ["Stack", "Queue", "Design"],
        "company_tags": ["Amazon", "Microsoft", "Bloomberg"],
        "statement_md": "Simulate a FIFO Queue using two stacks by executing a list of operations.\n\nOperations can be:\n- `[\"push\", x]`: pushes integer `x` to back of queue\n- `[\"pop\"]`: removes the element from front of queue and returns it\n- `[\"peek\"]`: returns element at front without removing\n- `[\"empty\"]`: returns boolean whether queue is empty\n\nGiven a list of commands, return a list of results (null for push, int or bool for pop/peek/empty).\n\n### Input Format\n- A JSON-encoded list of command arrays\n\n### Output Format\n- A JSON-encoded list of return values",
        "examples": [
            {
                "input": "[[\"push\", 1], [\"push\", 2], [\"peek\"], [\"pop\"], [\"empty\"]]",
                "output": "[null, null, 1, 1, false]",
                "explanation": "Queue is [1, 2]. Peek returns 1. Pop returns 1. Queue now has [2], empty is false."
            },
            {
                "input": "[[\"push\", 5], [\"pop\"], [\"empty\"]]",
                "output": "[null, 5, true]",
                "explanation": "Push 5, pop returns 5, queue is now empty."
            }
        ],
        "sample_tests": [
            {"input_text": "[[\"push\", 1], [\"push\", 2], [\"peek\"], [\"pop\"], [\"empty\"]]", "expected_output": "[null, null, 1, 1, false]"},
            {"input_text": "[[\"push\", 5], [\"pop\"], [\"empty\"]]", "expected_output": "[null, 5, true]"},
            {"input_text": "[[\"empty\"]]", "expected_output": "[true]"}
        ],
        "hidden_tests": [
            {"input_text": "[[\"push\", 10], [\"push\", 20], [\"push\", 30], [\"pop\"], [\"pop\"], [\"pop\"]]", "expected_output": "[null, null, null, 10, 20, 30]"},
            {"input_text": "[[\"push\", 1], [\"peek\"], [\"push\", 2], [\"peek\"]]", "expected_output": "[null, 1, null, 1]"},
            {"input_text": "[[\"push\", 7], [\"empty\"], [\"pop\"]]", "expected_output": "[null, false, 7]"},
            {"input_text": "[[\"push\", 1], [\"pop\"], [\"push\", 2], [\"pop\"]]", "expected_output": "[null, 1, null, 2]"},
            {"input_text": "[[\"push\", 99], [\"push\", 100], [\"peek\"], [\"pop\"], [\"empty\"]]", "expected_output": "[null, null, 99, 99, false]"},
            {"input_text": "[[\"push\", -5], [\"pop\"]]", "expected_output": "[null, -5]"},
            {"input_text": "[[\"push\", 0], [\"empty\"], [\"pop\"], [\"empty\"]]", "expected_output": "[null, false, 0, true]"},
            {"input_text": "[[\"push\", 3], [\"push\", 4], [\"pop\"], [\"push\", 5], [\"pop\"], [\"pop\"]]", "expected_output": "[null, null, 3, null, 4, 5]"},
            {"input_text": "[[\"push\", 8], [\"peek\"], [\"pop\"]]", "expected_output": "[null, 8, 8]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Maintain an in_stack for incoming items and an out_stack for outgoing items.", "xp_cost": 2},
            {"level": 2, "text": "Transfer elements from in_stack to out_stack only when out_stack is completely empty.", "xp_cost": 5},
            {"level": 3, "text": "Use Dual Stacks to achieve amortized O(1) time per queue operation.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Amortized Dual Stacks\n\nPush always appends to `in_stack`. For `pop` or `peek`, if `out_stack` is empty, pop all elements from `in_stack` and push them to `out_stack`. This reverses the order to FIFO. Each element moves at most twice.\n\n#### Complexity\n- **Time Complexity:** Amortized $O(1)$ per operation.\n- **Space Complexity:** $O(n)$ elements stored across stacks.\n\n#### Common Pitfalls\n- Transferring elements from `in_stack` before `out_stack` is empty (scrambles order).",
        "reference_solutions": {
            "brute_python": "def simulateQueue(ops):\n    q = []\n    res = []\n    for op in ops:\n        cmd = op[0]\n        if cmd == 'push': q.append(op[1]); res.append(None)\n        elif cmd == 'pop': res.append(q.pop(0))\n        elif cmd == 'peek': res.append(q[0])\n        elif cmd == 'empty': res.append(len(q) == 0)\n    return res",
            "optimal_python": "def simulateQueue(ops):\n    in_stk, out_stk = [], []\n    res = []\n    def transfer():\n        if not out_stk:\n            while in_stk: out_stk.append(in_stk.pop())\n    for op in ops:\n        cmd = op[0]\n        if cmd == 'push':\n            in_stk.append(op[1])\n            res.append(None)\n        elif cmd == 'pop':\n            transfer()\n            res.append(out_stk.pop())\n        elif cmd == 'peek':\n            transfer()\n            res.append(out_stk[-1])\n        elif cmd == 'empty':\n            res.append(len(in_stk) == 0 and len(out_stk) == 0)\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public List<Object> simulateQueue(List<List<Object>> ops) {\n        Stack<Integer> inStk = new Stack<>(), outStk = new Stack<>();\n        List<Object> res = new ArrayList<>();\n        for (List<Object> op : ops) {\n            String cmd = (String) op.get(0);\n            if (\"push\".equals(cmd)) {\n                inStk.push(((Number) op.get(1)).intValue());\n                res.add(null);\n            } else if (\"pop\".equals(cmd)) {\n                if (outStk.isEmpty()) while (!inStk.isEmpty()) outStk.push(inStk.pop());\n                res.add(outStk.pop());\n            } else if (\"peek\".equals(cmd)) {\n                if (outStk.isEmpty()) while (!inStk.isEmpty()) outStk.push(inStk.pop());\n                res.add(outStk.peek());\n            } else if (\"empty\".equals(cmd)) {\n                res.add(inStk.isEmpty() && outStk.isEmpty());\n            }\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <string>\n#include <stack>\nusing namespace std;\n// Reference simulation"
        }
    },

    # 27. Stack and Queue - Easy
    {
        "slug": "canonical-unix-path-normalizer",
        "title": "Canonical Unix Filepath Normalizer",
        "difficulty": "easy",
        "topic": "Stack and Queue",
        "tags": ["Stack", "String"],
        "company_tags": ["Meta", "Google", "Amazon"],
        "statement_md": "Given an absolute path for a Unix-style file system, which begins with a slash `'/'`, transform this path into its simplified canonical path.\n\nIn a Unix-style file system:\n- A single period `'.'` refers to the current directory.\n- A double period `'..'` refers to the directory up a level.\n- Multiple consecutive slashes are treated as a single slash `'/'`.\n\nThe canonical path must start with a single `'/'`, directories must be separated by exactly one `'/'`, and it must not end with a trailing `'/'` unless it is the root.\n\n### Input Format\n- A string `path`\n\n### Output Format\n- A string representing the canonical path",
        "examples": [
            {
                "input": "\"/home/\"",
                "output": "\"/home\"",
                "explanation": "Trailing slash is removed."
            },
            {
                "input": "\"/home//foo/\"",
                "output": "\"/home/foo\"",
                "explanation": "Multiple slashes are replaced by single slash."
            }
        ],
        "sample_tests": [
            {"input_text": "\"/home/\"", "expected_output": "\"/home\""},
            {"input_text": "\"/home//foo/\"", "expected_output": "\"/home/foo\""},
            {"input_text": "\"/home/user/Documents/../Pictures\"", "expected_output": "\"/home/user/Pictures\""}
        ],
        "hidden_tests": [
            {"input_text": "\"/../\"", "expected_output": "\"/\""},
            {"input_text": "\"/.../a/../b/c/../d/./\"", "expected_output": "\"/.../b/d\""},
            {"input_text": "\"/a/./b/../../c/\"", "expected_output": "\"/c\""},
            {"input_text": "\"/a/../../b/../c//.//\"", "expected_output": "\"/c\""},
            {"input_text": "\"/a//b////c/d//././/..\"", "expected_output": "\"/a/b/c\""},
            {"input_text": "\"/.\"", "expected_output": "\"/\""},
            {"input_text": "\"/..\"", "expected_output": "\"/\""},
            {"input_text": "\"/ready/2/code/../../arena\"", "expected_output": "\"/ready/arena\""},
            {"input_text": "\"/a/b/c/d/e/f/g\"", "expected_output": "\"/a/b/c/d/e/f/g\""}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Split the path by '/' delimiter to examine individual path tokens.", "xp_cost": 2},
            {"level": 2, "text": "Ignore empty strings and '.', pop from directory history on '..', otherwise push folder name.", "xp_cost": 5},
            {"level": 3, "text": "Use a LIFO Stack to track the current directory directory hierarchy.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Directory Token Stack\n\nSplit `path` by `/`. Iterate through tokens:\n- Ignore empty tokens and `.`\n- On `..`, pop from stack if stack is non-empty\n- For valid folder names, push to stack\nJoin stack elements with `/` prefixed by `/`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ tokenization and single scan.\n- **Space Complexity:** $O(n)$ stack storage.\n\n#### Common Pitfalls\n- Calling `..` at root directory should keep the path at `/` without popping into an error.",
        "reference_solutions": {
            "brute_python": "def simplifyPath(path):\n    parts = path.split('/')\n    stack = []\n    for p in parts:\n        if p == '' or p == '.': continue\n        if p == '..':\n            if stack: stack.pop()\n        else:\n            stack.append(p)\n    return '/' + '/'.join(stack)",
            "optimal_python": "def simplifyPath(path):\n    parts = path.split('/')\n    stack = []\n    for p in parts:\n        if p == '' or p == '.':\n            continue\n        elif p == '..':\n            if stack:\n                stack.pop()\n        else:\n            stack.append(p)\n    return '/' + '/'.join(stack)",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public String simplifyPath(String path) {\n        Deque<String> stack = new LinkedList<>();\n        for (String p : path.split(\"/\")) {\n            if (p.equals(\"\") || p.equals(\".\")) continue;\n            if (p.equals(\"..\")) {\n                if (!stack.isEmpty()) stack.pop();\n            } else {\n                stack.push(p);\n            }\n        }\n        List<String> list = new ArrayList<>(stack);\n        Collections.reverse(list);\n        return \"/\" + String.join(\"/\", list);\n    }\n}",
            "optimal_cpp": "#include <string>\n#include <vector>\n#include <sstream>\nusing namespace std;\nclass Solution {\npublic:\n    string simplifyPath(string path) {\n        stringstream ss(path);\n        string token;\n        vector<string> stack;\n        while (getline(ss, token, '/')) {\n            if (token == \"\" || token == \".\") continue;\n            if (token == \"..\") {\n                if (!stack.empty()) stack.pop_back();\n            } else {\n                stack.push_back(token);\n            }\n        }\n        string res = \"\";\n        for (const string& dir : stack) res += \"/\" + dir;\n        return res.empty() ? \"/\" : res;\n    }\n};"
        }
    },

    # 28. Stack and Queue - Medium
    {
        "slug": "next-warmer-temperature-wait-days",
        "title": "Daily Wait Time for Warmer Temperature",
        "difficulty": "medium",
        "topic": "Stack and Queue",
        "tags": ["Monotonic Stack", "Array"],
        "company_tags": ["Meta", "Amazon", "Google"],
        "statement_md": "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.\n\n### Input Format\n- A JSON-encoded list of integers `temperatures`\n\n### Output Format\n- A JSON-encoded list of integers `answer`",
        "examples": [
            {
                "input": "[73, 74, 75, 71, 69, 72, 76, 73]",
                "output": "[1, 1, 4, 2, 1, 1, 0, 0]",
                "explanation": "Day 0 (73) -> wait 1 day for 74. Day 2 (75) -> wait 4 days for 76."
            },
            {
                "input": "[30, 40, 50, 60]",
                "output": "[1, 1, 1, 0]",
                "explanation": "Every day has a warmer next day except the last."
            }
        ],
        "sample_tests": [
            {"input_text": "[73, 74, 75, 71, 69, 72, 76, 73]", "expected_output": "[1, 1, 4, 2, 1, 1, 0, 0]"},
            {"input_text": "[30, 40, 50, 60]", "expected_output": "[1, 1, 1, 0]"},
            {"input_text": "[30, 60, 90]", "expected_output": "[1, 1, 0]"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "[]"},
            {"input_text": "[80]", "expected_output": "[0]"},
            {"input_text": "[90, 80, 70, 60]", "expected_output": "[0, 0, 0, 0]"},
            {"input_text": "[50, 50, 50, 50]", "expected_output": "[0, 0, 0, 0]"},
            {"input_text": "[60, 50, 70]", "expected_output": "[2, 1, 0]"},
            {"input_text": "[35, 40, 38, 42, 30, 50]", "expected_output": "[1, 2, 1, 2, 1, 0]"},
            {"input_text": "[100, 99, 98, 97, 101]", "expected_output": "[4, 3, 2, 1, 0]"},
            {"input_text": "[20, 21, 22, 23]", "expected_output": "[1, 1, 1, 0]"},
            {"input_text": "[55, 60, 58, 65, 70]", "expected_output": "[1, 2, 1, 1, 0]"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Notice that you are seeking the next greater element to the right for each item.", "xp_cost": 2},
            {"level": 2, "text": "Store previous unresolved day indices in decreasing order of temperature.", "xp_cost": 5},
            {"level": 3, "text": "Use a Monotonic Decreasing Stack storing indices, popping indices when current temperature is strictly higher.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Monotonic Decreasing Stack\n\nMaintain a stack storing day indices. When iterating through day `i` with temperature `T`, while `stack` is non-empty and `temperatures[stack[-1]] < T`, pop `prev_idx` and record `res[prev_idx] = i - prev_idx`. Push `i` onto the stack.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each index pushed and popped at most once.\n- **Space Complexity:** $O(n)$ stack storage.\n\n#### Common Pitfalls\n- Storing temperature values in the stack instead of their indices.",
        "reference_solutions": {
            "brute_python": "def dailyTemperatures(temperatures):\n    n = len(temperatures)\n    res = [0] * n\n    for i in range(n):\n        for j in range(i + 1, n):\n            if temperatures[j] > temperatures[i]:\n                res[i] = j - i\n                break\n    return res",
            "optimal_python": "def dailyTemperatures(temperatures):\n    n = len(temperatures)\n    res = [0] * n\n    stack = []\n    for i, t in enumerate(temperatures):\n        while stack and temperatures[stack[-1]] < t:\n            prev = stack.pop()\n            res[prev] = i - prev\n        stack.append(i)\n    return res",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int[] dailyTemperatures(int[] temperatures) {\n        int n = temperatures.length;\n        int[] res = new int[n];\n        Stack<Integer> stack = new Stack<>();\n        for (int i = 0; i < n; i++) {\n            while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {\n                int prev = stack.pop();\n                res[prev] = i - prev;\n            }\n            stack.push(i);\n        }\n        return res;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <stack>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        int n = temperatures.size();\n        vector<int> res(n, 0);\n        stack<int> st;\n        for (int i = 0; i < n; i++) {\n            while (!st.empty() && temperatures[st.top()] < temperatures[i]) {\n                int prev = st.top();\n                st.pop();\n                res[prev] = i - prev;\n            }\n            st.push(i);\n        }\n        return res;\n    }\n};"
        }
    },

    # 29. Stack and Queue - Medium
    {
        "slug": "reverse-polish-notation-evaluator",
        "title": "Reverse Polish Notation Arithmetic Evaluator",
        "difficulty": "medium",
        "topic": "Stack and Queue",
        "tags": ["Stack", "Array", "Math"],
        "company_tags": ["Amazon", "LinkedIn", "Microsoft"],
        "statement_md": "You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.\n\nEvaluate the expression. Return an integer that represents the value of the expression.\n\nThe valid operators are `'+'`, `'-'`, `'*'`, and `'/'`. Each operand may be an integer or another expression. Division between two integers should truncate toward zero.\n\n### Input Format\n- A JSON-encoded list of strings `tokens`\n\n### Output Format\n- An integer representing the evaluated expression",
        "examples": [
            {
                "input": "[\"2\", \"1\", \"+\", \"3\", \"*\"]",
                "output": "9",
                "explanation": "((2 + 1) * 3) = 9"
            },
            {
                "input": "[\"4\", \"13\", \"5\", \"/\", \"+\"]",
                "output": "6",
                "explanation": "(4 + (13 / 5)) = 6 (13 / 5 = 2 truncated)"
            }
        ],
        "sample_tests": [
            {"input_text": "[\"2\", \"1\", \"+\", \"3\", \"*\"]", "expected_output": "9"},
            {"input_text": "[\"4\", \"13\", \"5\", \"/\", \"+\"]", "expected_output": "6"},
            {"input_text": "[\"10\", \"6\", \"9\", \"3\", \"+\", \"-11\", \"*\", \"/\", \"*\", \"17\", \"+\", \"5\", \"+\"]", "expected_output": "22"}
        ],
        "hidden_tests": [
            {"input_text": "[\"18\"]", "expected_output": "18"},
            {"input_text": "[\"3\", \"-4\", \"+\"]", "expected_output": "-1"},
            {"input_text": "[\"5\", \"2\", \"/\"]", "expected_output": "2"},
            {"input_text": "[\"-6\", \"3\", \"/\"]", "expected_output": "-2"},
            {"input_text": "[\"6\", \"-3\", \"/\"]", "expected_output": "-2"},
            {"input_text": "[\"0\", \"3\", \"/\"]", "expected_output": "0"},
            {"input_text": "[\"3\", \"4\", \"+\", \"5\", \"6\", \"+\", \"*\"]", "expected_output": "77"},
            {"input_text": "[\"10\", \"2\", \"-\"]", "expected_output": "8"},
            {"input_text": "[\"15\", \"7\", \"1\", \"1\", \"+\", \"-\", \"/\", \"3\", \"*\", \"2\", \"1\", \"1\", \"+\", \"+\", \"-\"]", "expected_output": "5"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "Push numbers onto the stack. When an operator is encountered, pop the last two numbers.", "xp_cost": 2},
            {"level": 2, "text": "Note that the first popped element is the right operand (b) and second is left (a): compute a op b.", "xp_cost": 5},
            {"level": 3, "text": "Use a LIFO Stack for operator evaluation, taking care of division truncation toward zero.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Postfix Stack Evaluation\n\nTraverse `tokens`. If token is a number, push to stack. If token is an operator, pop `b` then `a`. Compute `a op b` and push result back. For division in Python, use `int(a / b)` to truncate towards zero.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ single pass over tokens.\n- **Space Complexity:** $O(n)$ stack storage.\n\n#### Common Pitfalls\n- Truncation toward zero with negative operands (Python `//` floors towards $-\\infty$, so `int(a / b)` is required).",
        "reference_solutions": {
            "brute_python": "def evalRPN(tokens):\n    stack = []\n    for t in tokens:\n        if t == '+': stack.append(stack.pop() + stack.pop())\n        elif t == '*': stack.append(stack.pop() * stack.pop())\n        elif t == '-':\n            b, a = stack.pop(), stack.pop()\n            stack.append(a - b)\n        elif t == '/':\n            b, a = stack.pop(), stack.pop()\n            stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]",
            "optimal_python": "def evalRPN(tokens):\n    stack = []\n    for t in tokens:\n        if t == '+':\n            stack.append(stack.pop() + stack.pop())\n        elif t == '*':\n            stack.append(stack.pop() * stack.pop())\n        elif t == '-':\n            b = stack.pop()\n            a = stack.pop()\n            stack.append(a - b)\n        elif t == '/':\n            b = stack.pop()\n            a = stack.pop()\n            stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int evalRPN(String[] tokens) {\n        Stack<Integer> stack = new Stack<>();\n        for (String t : tokens) {\n            if (t.equals(\"+\")) stack.push(stack.pop() + stack.pop());\n            else if (t.equals(\"*\")) stack.push(stack.pop() * stack.pop());\n            else if (t.equals(\"-\")) {\n                int b = stack.pop(), a = stack.pop();\n                stack.push(a - b);\n            } else if (t.equals(\"/\")) {\n                int b = stack.pop(), a = stack.pop();\n                stack.push(a / b);\n            } else {\n                stack.push(Integer.parseInt(t));\n            }\n        }\n        return stack.pop();\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <string>\n#include <stack>\nusing namespace std;\nclass Solution {\npublic:\n    int evalRPN(vector<string>& tokens) {\n        stack<int> st;\n        for (const string& t : tokens) {\n            if (t == \"+\") { int b = st.top(); st.pop(); int a = st.top(); st.pop(); st.push(a + b); }\n            else if (t == \"*\") { int b = st.top(); st.pop(); int a = st.top(); st.pop(); st.push(a * b); }\n            else if (t == \"-\") { int b = st.top(); st.pop(); int a = st.top(); st.pop(); st.push(a - b); }\n            else if (t == \"/\") { int b = st.top(); st.pop(); int a = st.top(); st.pop(); st.push(a / b); }\n            else { st.push(stoi(t)); }\n        }\n        return st.top();\n    }\n};"
        }
    },

    # 30. Stack and Queue - Hard
    {
        "slug": "largest-rectangle-histogram-area",
        "title": "Largest Rectangular Area in Skyline Histogram",
        "difficulty": "hard",
        "topic": "Stack and Queue",
        "tags": ["Monotonic Stack", "Array"],
        "company_tags": ["Amazon", "Google", "Meta", "Uber"],
        "statement_md": "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.\n\n### Input Format\n- A JSON-encoded list of integers `heights`\n\n### Output Format\n- An integer representing maximum rectangular area",
        "examples": [
            {
                "input": "[2, 1, 5, 6, 2, 3]",
                "output": "10",
                "explanation": "The largest rectangle is formed between bars of height 5 and 6 with min height 5 and width 2 (5 * 2 = 10)."
            },
            {
                "input": "[2, 4]",
                "output": "4",
                "explanation": "Bar of height 4 with width 1 = 4."
            }
        ],
        "sample_tests": [
            {"input_text": "[2, 1, 5, 6, 2, 3]", "expected_output": "10"},
            {"input_text": "[2, 4]", "expected_output": "4"},
            {"input_text": "[1]", "expected_output": "1"}
        ],
        "hidden_tests": [
            {"input_text": "[]", "expected_output": "0"},
            {"input_text": "[0]", "expected_output": "0"},
            {"input_text": "[5, 5, 5, 5, 5]", "expected_output": "25"},
            {"input_text": "[1, 2, 3, 4, 5]", "expected_output": "9"},
            {"input_text": "[5, 4, 3, 2, 1]", "expected_output": "9"},
            {"input_text": "[6, 2, 5, 4, 5, 1, 6]", "expected_output": "12"},
            {"input_text": "[2, 1, 2]", "expected_output": "3"},
            {"input_text": "[100, 200, 100]", "expected_output": "300"},
            {"input_text": "[3, 6, 5, 7, 4, 8, 1, 0]", "expected_output": "20"}
        ],
        "time_limit_ms": 1000,
        "memory_limit_mb": 128,
        "hints": [
            {"level": 1, "text": "For each bar, what is the furthest it can extend to the left and to the right while maintaining its height?", "xp_cost": 2},
            {"level": 2, "text": "Maintain an increasing stack of indices. When a shorter bar is found, calculate rectangles for bars that can no longer extend.", "xp_cost": 5},
            {"level": 3, "text": "Use a Monotonic Increasing Stack to calculate the maximal width bounded by the nearest smaller elements on left and right.", "xp_cost": 10}
        ],
        "editorial_md": "### Optimal Approach: Monotonic Increasing Stack\n\nPush sentinel 0 at the end of `heights`. Maintain a stack of indices with increasing heights. When `heights[i]` is less than top bar, pop height `h`. The width extends from current `i` back to `stack[-1]`: `width = i if not stack else i - stack[-1] - 1`. Maximize `h * width`.\n\n#### Complexity\n- **Time Complexity:** $O(n)$ each index pushed and popped once.\n- **Space Complexity:** $O(n)$ stack storage.\n\n#### Common Pitfalls\n- Not clearing the stack at the end (mitigated cleanly by appending height 0 sentinel).",
        "reference_solutions": {
            "brute_python": "def largestRectangleArea(heights):\n    max_area = 0\n    n = len(heights)\n    for i in range(n):\n        min_h = heights[i]\n        for j in range(i, n):\n            min_h = min(min_h, heights[j])\n            max_area = max(max_area, min_h * (j - i + 1))\n    return max_area",
            "optimal_python": "def largestRectangleArea(heights):\n    stack = []\n    max_area = 0\n    extended = heights + [0]\n    for i, h in enumerate(extended):\n        while stack and extended[stack[-1]] > h:\n            height = extended[stack.pop()]\n            width = i if not stack else i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    return max_area",
            "optimal_java": "import java.util.*;\npublic class Solution {\n    public int largestRectangleArea(int[] heights) {\n        Stack<Integer> stack = new Stack<>();\n        int maxArea = 0;\n        int n = heights.length;\n        for (int i = 0; i <= n; i++) {\n            int h = (i == n) ? 0 : heights[i];\n            while (!stack.isEmpty() && heights[stack.peek()] > h) {\n                int height = heights[stack.pop()];\n                int width = stack.isEmpty() ? i : i - stack.peek() - 1;\n                maxArea = Math.max(maxArea, height * width);\n            }\n            stack.push(i);\n        }\n        return maxArea;\n    }\n}",
            "optimal_cpp": "#include <vector>\n#include <stack>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    int largestRectangleArea(vector<int>& heights) {\n        stack<int> st;\n        int maxArea = 0;\n        int n = heights.size();\n        for (int i = 0; i <= n; i++) {\n            int h = (i == n) ? 0 : heights[i];\n            while (!st.empty() && heights[st.top()] > h) {\n                int height = heights[st.top()];\n                st.pop();\n                int width = st.empty() ? i : i - st.top() - 1;\n                maxArea = max(maxArea, height * width);\n            }\n            st.push(i);\n        }\n        return maxArea;\n    }\n};"
        }
    }
]

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "content", "problems")
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for p in PROBLEMS:
        fpath = os.path.join(out_dir, f"{p['slug']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
        count += 1
    print(f"Batch 3 generated {count} problems.")

if __name__ == "__main__":
    main()
