from unstructured.partition.auto import partition
from unstructured.documents.elements import NarrativeText, Title
import keyboard
import argparse
from tqdm import tqdm
import os

def print_sentence(idx, flat_sentences):
    os.system('clear')
    print(f"{idx+1} / {len(flat_sentences)}")
    print(flat_sentences[idx])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts text from a PDF file and prints it to the console by sentences."
    )
    parser.add_argument("--file", type=str, default='input/2305.14824.pdf',help="The PDF file to extract text from.")
    # not implemented here
    parser.add_argument("--resume_file", type=str, default="input/resume/2305.14824.json", help="The file to save the current state of the document.")
    parser.add_argument("--resume", type=bool, default=False, help="Resume from where you left off.")
    parser.add_argument("--save", type=bool, default=False, help="Save the current state of the document.")
    args = parser.parse_args()

    elements = partition(args.file)
    narratives = [i for i in elements if type(i) == NarrativeText or type(i) == Title]

    # we need a generator to iterate over the narratives in an efficient way
    flat_sentences = list()

    # split narratives into sentences and print them to the console\
    # we can also save the current state of the document and resume from where we left off
    print('Flatting into sentences...')
    for idx, nar in tqdm(enumerate(narratives)):
        sentences = nar.__str__().split(".")
        for sent in sentences:
            flat_sentences.append(sent)

    idx = 0
    while True:
        try:
            if keyboard.is_pressed("a"):
                assert idx < 0, "You are at the beginning of the document."
                idx -= 1
                print_sentence(idx, flat_sentences)

            elif keyboard.is_pressed("d"):
                idx += 1
                print_sentence(idx, flat_sentences)

            if idx == len(flat_sentences):
                print("You have reached the end of the document.")
                quit()
        except KeyboardInterrupt:
            # we save the current state of the document
            quit()
            # we can resume from where we left off
    
    # we should also be able to go back to the previous sentence by pressing a key