import random
import asyncio
import deepl

# 文件路径
file_path = 'data.txt'
memory_file_path = 'memory.txt'

# 使用Google翻译API
auth_key = "4ba98537-f84f-490c-bf39-2435a1884b79:fx"
translator = deepl.Translator(auth_key)


# 读取文件中的单词表
def read_words():
    words = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    english, chinese = line.strip().split(',')
                    words[english] = chinese
    except FileNotFoundError:
        pass
    return words


# 将单词保存到文件
def save_words(words):
    with open(file_path, 'w', encoding='utf-8') as f:
        for english, chinese in words.items():
            f.write(f'{english},{chinese}\n')


# 读取记忆情况和熟悉度
def read_memory():
    try:
        with open(memory_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            memory = {}
            for line in lines:
                # 忽略空行和格式不正确的行
                line = line.strip()
                if line and ',' in line:
                    try:
                        word, score = line.split(',')
                        memory[word] = int(score)
                    except ValueError:
                        print(f"忽略无效行: {line}")
    except FileNotFoundError:
        memory = {}
    return memory

# 更新记忆情况
def update_memory(memory):
    with open(memory_file_path, 'w', encoding='utf-8') as f:
        for word, score in memory.items():
            f.write(f'{word},{score}\n')


# 获取中文翻译，使用异步
async def get_chinese_translation(english):
    try:
        translation = translator.translate_text(english, target_lang="ZH")
        return translation.text
    except Exception as e:
        print(f"翻译失败: {e}")
        return ""


# 添加单词
async def add_word():
    words = read_words()
    english = input("请输入英文单词: ").strip()

    # 自动生成中文翻译
    chinese = await get_chinese_translation(english)

    if chinese:
        if english in words:
            print(f"单词 {english} 已经存在！")
        else:
            words[english] = chinese
            save_words(words)
            print(f"单词 {english} 添加成功！中文意思是: {chinese}")
    else:
        print("翻译失败，单词未添加！")


# 删除单词
def delete_word():
    words = read_words()
    english = input("请输入要删除的英文单词: ").strip()

    if english in words:
        del words[english]
        save_words(words)
        print(f"单词 {english} 删除成功！")
    else:
        print(f"单词 {english} 不存在！")


# 抽查功能
def quiz():
    words = read_words()
    memory = read_memory()

    # 如果记忆为空，则初始化所有单词的熟悉度为 0
    if not memory:
        memory = {english: 0 for english in words}

    while True:
        # 按照熟悉度排序，熟悉度值低的优先
        sorted_words = sorted(memory.items(), key=lambda x: x[1])

        # 从熟悉度值最小的单词中随机选择一个
        english, _ = random.choice(sorted_words)
        print(f"你知道 {english} 的中文意思吗？")
        user_answer = input("请输入 '1' 如果知道, 否则输入 '0'。输入 'q' 退出抽查: ").strip().lower()

        if user_answer == 'q':
            break
        elif user_answer == '0':
            memory[english] -= 1  # 不认识，熟悉度减 1
            print(f"正确答案是: {words[english]}")
        elif user_answer == '1':
            memory[english] += 1  # 认识，熟悉度加 1
        else:
            print("输入无效，请输入 '1'、'0' 或 'q'。")

        # 更新记忆情况
        update_memory(memory)


# 主菜单
async def main():
    while True:
        print("\n请选择操作:")
        print("1. 添加单词")
        print("2. 删除单词")
        print("3. 抽查单词")
        print("4. 退出")

        choice = input("请输入选项(1-4): ").strip()

        if choice == '1':
            await add_word()
        elif choice == '2':
            delete_word()
        elif choice == '3':
            quiz()
        elif choice == '4':
            break
        else:
            print("无效选项，请重新输入!")


if __name__ == "__main__":
    asyncio.run(main())
