import sys

from crawlers.ganjoor import GanjoorCrawler
from crawlers.ganjoor_client import GanjoorClient

from storage.raw_storage import RawStorage
from storage.state_storage import StateStorage

from processors.poem_processor import PoemProcessor
from dataset.exporter import DatasetExporter

from tokenizer.train_tokenizer import TokenizerTrainer

from tokenizer.tokenize_dataset import DatasetTokenizer
from training.build_bins import BinBuilder

def build_crawler():
    return GanjoorCrawler(
        GanjoorClient(),
        RawStorage(),
        StateStorage()
    )


def build_processor():
    return PoemProcessor(
        RawStorage()
    )


def build_exporter():
    return DatasetExporter(    )

def build_train_tokenizer():
    return TokenizerTrainer()

def build_tokenizer():
    return DatasetTokenizer()

def build_bins():
    return BinBuilder()


def main():

    if len(sys.argv) < 2:
        print(
            """
Commands:

crawl_all
process
export
pipeline
train_tokenizer
tokenize
build_bins
train
"""
        )
        return

    command = sys.argv[1]

    if command == "crawl_all":

        crawler = build_crawler()
        crawler.crawl_all()

    elif command == "process":

        processor = build_processor()
        processor.process_all()

    elif command == "export":

        exporter = build_exporter()
        exporter.export()

    elif command == "pipeline":

        crawler = build_crawler()
        crawler.crawl_all()

        processor = build_processor()
        processor.process_all()

        exporter = build_exporter()
        exporter.export()
        
    elif command == "train_tokenizer":
        trainer = build_train_tokenizer()
        trainer.train()
        
    elif command == "tokenize":
        tokenizer = build_tokenizer()
        tokenizer.run()

    elif command == "build_bins":
        builder = build_bins()
        builder.run()

    elif command == "train":
        from training.train import train
        train()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()