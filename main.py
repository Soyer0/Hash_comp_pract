import hashlib
import random
import string
import numpy as np
import matplotlib.pyplot as plt


def find_preimage(message="GilevskiyOlexanderMikolayovich"):
    original_hash = hashlib.sha384(message.encode()).hexdigest()

    i = 0
    modifications = [message]
    hash_modifications = [color_last_four(original_hash)]

    messages_generated = []
    while True:
        modified_message = message + str(i)
        modified_hash = hashlib.sha384(modified_message.encode()).hexdigest()
        i += 1

        modifications.append(modified_message)
        hash_modifications.append(color_last_four(modified_hash))

        if modified_hash[-4:] == original_hash[-4:]:
            messages_generated.append(i)
            record_info("Find preimage", message, modifications[:30] + [modified_message],
                        hash_modifications[:30] + [color_last_four(modified_hash)], i)
            break

    return i


def find_preimage_random_modifications(message="GilevskiyOlexanderMikolayovich"):
    original_hash = hashlib.sha384(message.encode()).hexdigest()
    modified_message = message
    i = 0
    modifications = [message]
    hash_modifications = [color_last_four(original_hash)]

    while True:
        i += 1

        index = random.randint(0, len(message) - 1)
        replacement = random.choice(string.printable)
        while replacement == "\n" or replacement == " " or replacement == modified_message[index]:
            replacement = random.choice(string.printable)
        modified_message = modified_message[:index] + replacement + modified_message[index + 1:]
        modified_hash = hashlib.sha384(modified_message.encode()).hexdigest()

        modifications.append(modified_message)
        hash_modifications.append(color_last_four(modified_hash))

        if modified_hash[-4:] == original_hash[-4:]:
            # record_info("Find preimage random modifications", message, modifications[:30] + [modified_message],
            #             hash_modifications[:30] + [color_last_four(modified_hash)], i)
            break

    return i


def first_birthday_attack(message="GilevskiyOlexanderMikolayovichFI-03"):
    original_hash = hashlib.sha384(message.encode()).hexdigest()

    i = 0
    hash_dict = {original_hash[-8:]: original_hash}

    modifications = [message]
    hash_modifications = [color_last_eight(original_hash)]

    while True:
        modified_message = message + str(i)
        modified_hash = hashlib.sha384(modified_message.encode()).hexdigest()
        i += 1

        modifications.append(modified_message)
        hash_modifications.append(color_last_eight(modified_hash))

        if modified_hash[-8:] in hash_dict:
            collision_message = (list(hash_dict).index(modified_hash[-8:]), modified_message, color_last_eight(hash_dict[modified_hash[-8:]]))
            record_info("First birthday attack", message, modifications[:30] + [modified_message],
                        hash_modifications[:30] + [color_last_eight(modified_hash)], i,  collision_message)
            break

        if modified_hash[-8:] not in hash_dict:
            hash_dict[modified_hash[-8:]] = modified_hash

    return i


def second_birthday_attack(message="GilevskiyOlexanderMikolayovichFI-03"):
    original_hash = hashlib.sha384(message.encode()).hexdigest()
    modified_message = message

    hash_dict = {original_hash[-8:]: original_hash}

    modifications = [message]
    hash_modifications = [color_last_eight(original_hash)]
    i = 0
    while True:
        i += 1

        index = random.randint(0, len(message) - 1)
        replacement = random.choice(string.printable)
        while replacement in ["\n", " ", modified_message[index]]:
            replacement = random.choice(string.printable)
        modified_message = modified_message[:index] + replacement + modified_message[index + 1:]
        modified_hash = hashlib.sha384(modified_message.encode()).hexdigest()

        modifications.append(modified_message)
        hash_modifications.append(color_last_eight(modified_hash))

        if modified_hash[-8:] in hash_dict and modified_hash != hash_dict[modified_hash[-8:]]:
            collision_message = (list(hash_dict).index(modified_hash[-8:]), modified_message, color_last_eight(hash_dict[modified_hash[-8:]]))
            # record_info("Second birthday attack", message, modifications[:30] + [modified_message],
            #             hash_modifications[:30] + [color_last_eight(modified_hash)], i, collision_message)
            break

        if modified_hash[-8:] not in hash_dict:
            hash_dict[modified_hash[-8:]] = modified_hash

    return i


def color_last_four(text):
    if len(text) >= 4:
        colored_text = text[:-4] + "\033[95m" + text[-4:] + "\033[0m"
        return colored_text
    else:
        return text


def color_last_eight(text):
    if len(text) >= 8:
        colored_text = text[:-8] + "\033[95m" + text[-8:] + "\033[0m"
        return colored_text
    else:
        return text


def record_info(function_name, message, modifications, hash_modifications, iteration_num, collision_message=None):
    print(f"Attack: {function_name}")
    print(f"Message: {message}")
    print("Modifications:")
    if iteration_num > 30:
        for i in range(30):
            print(f"{i + 1}. {modifications[i]} -- {hash_modifications[i]}")
        if collision_message is not None:
            print(f"{collision_message[0]}. {collision_message[1]} -- {collision_message[2]}")
            print(f"{iteration_num}. {modifications[30]} -- {hash_modifications[30]}")
        else:
            print(f"{iteration_num}. {modifications[30]} -- {hash_modifications[30]}")
    else:
        for i in range(iteration_num + 1):
            print(f"{i + 1}. {modifications[i]}")
    print("=================================\n\n")


def plot_iterations(attacks, num_runs):
    for attack_idx, attack in enumerate(attacks, start=1):
        plt.figure(figsize=(10, 6))
        plt.xlabel('Кількість ітерацій')
        plt.ylabel('№ випадку')

        iterations_list = []

        for _ in range(num_runs):
            iterations = attack()
            iterations_list.append(iterations)

        # Побудова стовпчикової діаграми для кожної атаки
        num_iterations = [iterations if isinstance(iterations, int) else max(iterations) for iterations in iterations_list]
        plt.bar(range(len(num_iterations)), num_iterations, label=f'Attack {attack_idx}')

        avg_iterations = np.mean(num_iterations)
        variance_iterations = np.var(num_iterations)
        confidence_interval = np.percentile(num_iterations, [2.5, 97.5])

        print(f'Attack {attack_idx}:')
        print(f'Attack {attack_idx}:')
        print(f'Середнє значення: {avg_iterations}')
        print(f'Дисперсія: {variance_iterations}')
        print(f'Довірчий інтервал: {confidence_interval[0]} - {confidence_interval[1]}')

        plt.legend()
        plt.show()


def main():
    # find_preimage()
    # find_preimage_random_modifications()
    # first_birthday_attack()
    # second_birthday_attack()

    attacks_list = [find_preimage_random_modifications, second_birthday_attack]

    plot_iterations(attacks_list, num_runs=100)


if __name__ == "__main__":
    main()
