import sys

from crawlers.ganjoor import GanjoorCrawler
from crawlers.ganjoor_client import GanjoorClient

from storage.raw_storage import RawStorage
from storage.state_storage import StateStorage

from processors.poem_processor import PoemProcessor
from dataset.exporter import DatasetExporter

from tokenizer.train_tokenizer import TokenizerTrainer

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
        
    elif "train_tokenizer":
        trainer = build_train_tokenizer()
        trainer.train()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()