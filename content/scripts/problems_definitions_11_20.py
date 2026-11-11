from collections import Counter, defaultdict
import random

def add_problems_11_20(register):
    # 11. Longest Substring with At Most K Distinct Characters
    def sol_k_distinct(s, k):
        if not s or k == 0:
            return 0
        left = 0
        max_len = 0
        counts = defaultdict(int)
        for right, char in enumerate(s):
            counts[char] += 1
            while len(counts) > k:
                counts[s[left]] -= 1
                if counts[s[left]] == 0:
                    del counts[s[left]]
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len

    def gen_k_distinct(rng):
        n = rng.randint(2, 20)
        s = "".join(rng.choice("abcdef") for _ in range(n))
        k = rng.randint(1, 4)
        return [s, k]

    register(
        slug="k-distinct-substring",
        title="Longest Substring with At Most K Distinct Characters",
        topic_key="two_pointers",
        diff="medium",
        statement="Given a string `s` and an integer `k`, return the length of the longest substring that contains at most `k` distinct characters.",
        fn="lengthOfLongestSubstringKDistinct",
        params=["s", "k"],
        examples=[
            [["eceba", 2], 3],
            [["aa", 1], 2]
        ],
        sol=sol_k_distinct,
        gen=gen_k_distinct
    )

    # 12. Subarray Product Less Than K
    def sol_subarray_product(nums, k):
        if k <= 1:
            return 0
        prod = 1
        ans = left = 0
        for right, val in enumerate(nums):
            prod *= val
            while prod >= k and left <= right:
                prod //= nums[left]
                left += 1
            ans += right - left + 1
        return ans

    def gen_subarray_product(rng):
        n = rng.randint(3, 15)
        nums = [rng.randint(1, 10) for _ in range(n)]
        k = rng.randint(5, 100)
        return [nums, k]

    register(
        slug="subarray-product-less-k",
        title="Subarray Product Less Than K",
        topic_key="two_pointers",
        diff="medium",
        statement="Given an array of positive integers `nums` and an integer `k`, return the number of contiguous subarrays where the product of all elements is strictly less than `k`.",
        fn="numSubarrayProductLessThanK",
        params=["nums", "k"],
        examples=[
            [[[10, 5, 2, 6], 100], 8],
            [[[1, 2, 3], 0], 0]
        ],
        sol=sol_subarray_product,
        gen=gen_subarray_product
    )

    # 13. Count and Say
    def sol_count_and_say(n):
        res = "1"
        for _ in range(n - 1):
            next_res = []
            i = 0
            while i < len(res):
                count = 1
                while i + 1 < len(res) and res[i] == res[i + 1]:
                    i += 1
                    count += 1
                next_res.append(str(count) + res[i])
                i += 1
            res = "".join(next_res)
        return res

    def gen_count_and_say(rng):
        n = rng.randint(1, 12)
        return [n]

    register(
        slug="count-and-say",
        title="Count and Say",
        topic_key="strings",
        diff="medium",
        statement="The count-and-say sequence is defined recursively: `countAndSay(1) = '1'`, and `countAndSay(n)` is the run-length encoding of `countAndSay(n - 1)`. Given a positive integer `n`, return the `n`-th term of the sequence.",
        fn="countAndSay",
        params=["n"],
        examples=[
            [[1], "1"],
            [[4], "1211"]
        ],
        sol=sol_count_and_say,
        gen=gen_count_and_say
    )

    # 14. Zigzag Conversion
    def sol_zigzag(s, numRows):
        if numRows == 1 or numRows >= len(s):
            return s
        rows = [[] for _ in range(numRows)]
        idx = 0
        step = 1
        for ch in s:
            rows[idx].append(ch)
            if idx == 0:
                step = 1
            elif idx == numRows - 1:
                step = -1
            idx += step
        return "".join("".join(row) for row in rows)

    def gen_zigzag(rng):
        n = rng.randint(3, 20)
        s = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n))
        numRows = rng.randint(1, 5)
        return [s, numRows]

    register(
        slug="zigzag-conversion",
        title="Zigzag Conversion",
        topic_key="strings",
        diff="medium",
        statement="The string `s` is written in a zigzag pattern on a given number of rows `numRows`. Read line by line and return the resulting converted string.",
        fn="convert",
        params=["s", "numRows"],
        examples=[
            [["PAYPALISHIRING", 3], "PAHNAPLSIIGYIR"],
            [["PAYPALISHIRING", 4], "PINALSIGYAHRPI"],
            [["A", 1], "A"]
        ],
        sol=sol_zigzag,
        gen=gen_zigzag
    )

    # 15. Reverse Vowels of a String
    def sol_rev_vowels(s):
        vowels = set("aeiouAEIOU")
        arr = list(s)
        i, j = 0, len(arr) - 1
        while i < j:
            if arr[i] not in vowels:
                i += 1
            elif arr[j] not in vowels:
                j -= 1
            else:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        return "".join(arr)

    def gen_rev_vowels(rng):
        n = rng.randint(3, 20)
        chars = "abcdefghijklmnopqrstuvwxyzAEIOU"
        s = "".join(rng.choice(chars) for _ in range(n))
        return [s]

    register(
        slug="reverse-vowels",
        title="Reverse Vowels of a String",
        topic_key="strings",
        diff="easy",
        statement="Given a string `s`, reverse only all the vowels in the string and return it. The vowels are 'a', 'e', 'i', 'o', 'u' (both lower and upper case).",
        fn="reverseVowels",
        params=["s"],
        examples=[
            [["hello"], "holle"],
            [["leetcode"], "leotcede"]
        ],
        sol=sol_rev_vowels,
        gen=gen_rev_vowels
    )

    # 16. Excel Sheet Column Number
    def sol_excel_col(columnTitle):
        ans = 0
        for ch in columnTitle:
            ans = ans * 26 + (ord(ch) - ord('A') + 1)
        return ans

    def gen_excel_col(rng):
        l = rng.randint(1, 4)
        col = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(l))
        return [col]

    register(
        slug="excel-column-number",
        title="Excel Sheet Column Number",
        topic_key="strings",
        diff="easy",
        statement="Given a string `columnTitle` that represents the column title as appears in an Excel sheet, return its corresponding column number (e.g. 'A' -> 1, 'Z' -> 26, 'AA' -> 27).",
        fn="titleToNumber",
        params=["columnTitle"],
        examples=[
            [["A"], 1],
            [["AB"], 28],
            [["ZY"], 701]
        ],
        sol=sol_excel_col,
        gen=gen_excel_col
    )

    # 17. Minimum Remove to Make Valid Parentheses
    def sol_min_remove_parens(s):
        indexes_to_remove = set()
        stack = []
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            elif ch == ')':
                if stack:
                    stack.pop()
                else:
                    indexes_to_remove.add(i)
        indexes_to_remove = indexes_to_remove.union(set(stack))
        return "".join(ch for i, ch in enumerate(s) if i not in indexes_to_remove)

    def gen_min_remove_parens(rng):
        chars = "()abc"
        n = rng.randint(3, 20)
        s = "".join(rng.choice(chars) for _ in range(n))
        return [s]

    register(
        slug="min-remove-valid-parentheses",
        title="Minimum Remove to Make Valid Parentheses",
        topic_key="strings",
        diff="medium",
        statement="Given a string `s` of `'('`, `')'` and lowercase characters, remove the minimum number of parentheses so that the resulting parentheses string is valid.",
        fn="minRemoveToMakeValid",
        params=["s"],
        examples=[
            [["lee(t(c)o)de)"], "lee(t(c)o)de"],
            [["a)b(c)d"], "ab(c)d"],
            [[")("], ""]
        ],
        sol=sol_min_remove_parens,
        gen=gen_min_remove_parens
    )

    # 18. Repeated DNA Sequences
    def sol_dna(s):
        seen = set()
        repeated = set()
        for i in range(len(s) - 9):
            sub = s[i:i+10]
            if sub in seen:
                repeated.add(sub)
            else:
                seen.add(sub)
        return sorted(list(repeated))

    def gen_dna(rng):
        bases = "ACGT"
        n = rng.randint(12, 35)
        s = "".join(rng.choice(bases) for _ in range(n))
        return [s]

    register(
        slug="repeated-dna-sequences",
        title="Repeated DNA Sequences",
        topic_key="strings",
        diff="medium",
        statement="Given a string `s` that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. Return the list in ascending lexicographical order.",
        fn="findRepeatedDnaSequences",
        params=["s"],
        examples=[
            [["AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"], ["AAAAACCCCC", "CCCCCAAAAA"]],
            [["AAAAAAAAAAAAA"], ["AAAAAAAAAA"]]
        ],
        sol=sol_dna,
        gen=gen_dna
    )

    # 19. Basic Calculator II
    def sol_calc_ii(s):
        stack = []
        num = 0
        op = '+'
        s = s.replace(" ", "")
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            if not ch.isdigit() or i == len(s) - 1:
                if op == '+':
                    stack.append(num)
                elif op == '-':
                    stack.append(-num)
                elif op == '*':
                    stack.append(stack.pop() * num)
                elif op == '/':
                    top = stack.pop()
                    if top < 0:
                        stack.append(-(-top // num))
                    else:
                        stack.append(top // num)
                op = ch
                num = 0
        return sum(stack)

    def gen_calc_ii(rng):
        nums = [rng.randint(1, 20) for _ in range(rng.randint(2, 5))]
        ops = [rng.choice(['+', '-', '*', '/']) for _ in range(len(nums) - 1)]
        expr = []
        for i in range(len(nums)):
            expr.append(str(nums[i]))
            if i < len(ops):
                expr.append(ops[i])
        return ["".join(expr)]

    register(
        slug="basic-calculator-ii",
        title="Basic Calculator II",
        topic_key="stack",
        diff="medium",
        statement="Given a string `s` representing an expression of non-negative integers and operators `'+'`, `'-'`, `'*'`, `'/'`, evaluate the expression. Integer division should truncate toward zero.",
        fn="calculate",
        params=["s"],
        examples=[
            [["3+2*2"], 7],
            [[" 3/2 "], 1],
            [[" 3+5 / 2 "], 5]
        ],
        sol=sol_calc_ii,
        gen=gen_calc_ii
    )

    # 20. Remove K Digits
    def sol_remove_k_digits(num, k):
        stack = []
        for d in num:
            while k > 0 and stack and stack[-1] > d:
                stack.pop()
                k -= 1
            stack.append(d)
        if k > 0:
            stack = stack[:-k]
        res = "".join(stack).lstrip('0')
        return res if res else "0"

    def gen_remove_k_digits(rng):
        n = rng.randint(2, 15)
        num = "".join(str(rng.randint(1 if i == 0 else 0, 9)) for i in range(n))
        k = rng.randint(1, n - 1)
        return [num, k]

    register(
        slug="remove-k-digits",
        title="Remove K Digits",
        topic_key="stack",
        diff="medium",
        statement="Given string `num` representing a non-negative integer and an integer `k`, return the smallest possible integer after removing `k` digits from `num`. Leading zeros should be stripped; return `'0'` if empty.",
        fn="removeKdigits",
        params=["num", "k"],
        examples=[
            [["1432219", 3], "1219"],
            [["10200", 1], "200"],
            [["10", 2], "0"]
        ],
        sol=sol_remove_k_digits,
        gen=gen_remove_k_digits
    )
