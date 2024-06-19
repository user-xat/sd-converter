import argparse
import os
import sys
import logging
import recognizers.model_recognizer as model_recognizer
from model.model import SDModel
from xmi_writers.visual_paradigm.writer import write as vp_writer
from xmi_writers.genmymodel.writer import write as gm_writer


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sd2xmi", description="sd2xmi is a program for converting a UML sequence diagram image to an XMI file.")

    parser.add_argument("images", metavar="IMG", nargs="+", help="Image or images to convert")
    parser.add_argument("-tp", "--target-program", default="VisualParadigm", choices=["VisualParadigm", "GenMyModel"], help="The target program for which you want to generate an XMI file (default: VisualParadigm).")
    parser.add_argument("-ic", "--intersection-coefficient", metavar="NUM", type=float, default=0.8, help="If the coefficient of intersection of the areas occupied by the elements is greater than the specified one, then one of the elements becomes a child of the other. The value must be between 0 and 1 (default=0.8).")
    parser.add_argument("-ml", "--ml-model", metavar="FILE", default="sd_model.pt", help="The path to the file of the model used to recognize elements in the sd diagram.")
    parser.add_argument("--log", help="Creates log file", action="store_true")
    parser.add_argument("--log-file", metavar="FILE", default="sd2xmi.log", help="Specify the filepath of the log file.")
    parser.add_argument("--verbose", help="Explain what is being done", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1")

    return parser

def check_parameters(args: argparse.ArgumentParser):
    try:
        if not os.path.isfile(args.ml_model):
            raise FileNotFoundError(f'{args.ml_model} is not found')
        if not (0 <= args.intersection_coefficient <= 1):
            raise ValueError('the intersection_coefficient must be must be between 0 and 1')
        if args.target_program.casefold() == "genmymodel":
            raise ValueError('genmymodel is not supported yet')
    except Exception as err:
        logging.exception(err)
        raise err

def setup_logger(args):
    handlers = []
    if args.log:
        handlers.append(logging.FileHandler(args.log_file, 'w'))
    if args.verbose:
        handlers.append(logging.StreamHandler())
    if len(handlers) == 0:
        logging.disable(logging.CRITICAL)

    logging.root.handlers = [] # необходимо, иначе handlers не применяются
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers)

def get_models(results: list, coef: float) -> list[SDModel]:
    models: list[SDModel] = list()
    for res in results:
        models.append(SDModel.make(res, coef))
    return models

def debug_main() -> None:
    args = {"imges": ['img/example2.png'], "target_program": 'VisualParadigm', "output_file":'model.xmi', "intersection_coefficient": 0.75, "ml_model":'sd_model.pt'}

    results = model_recognizer.recognize(args["ml_model"], args["imges"])
    models = get_models(results, args["intersection_coefficient"])

    for i, model in enumerate(models):
        model.create_model()
        if i > 0:
            output_file = f"{i}{args['output_file']}"
        else:
            output_file = args['output_file']

        if args['target_program'].casefold() == "visualparadigm":
            vp_writer(output_file, model)
        elif args['target_program'].casefold() == "genmymodel":
            gm_writer(output_file, model)

def main(args: argparse.Namespace):
    results = model_recognizer.recognize(args.ml_model, args.images, args.verbose)
    models = get_models(results, args.intersection_coefficient)

    for i, model in enumerate(models):
        filename, _ = os.path.splitext(args.images[i])
        model.create_model()
        output_file = f"{filename}.xmi"

        if args.target_program.casefold() == "visualparadigm":
            vp_writer(output_file, model)
        elif args.target_program.casefold() == "genmymodel":
            gm_writer(output_file, model)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    setup_logger(args)
    check_parameters(args)
    # debug_main()
    main(args)