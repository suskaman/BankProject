from utils import get_data_from_excel

def main() -> None:
    data = get_data_from_excel("data/operations.xlsx")
    print(data)

    return None


if __name__ == "__main__":
    main()
