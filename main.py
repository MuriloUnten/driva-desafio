import csv
import pandas as pd
import matplotlib.pyplot as plt

PRODUCTS = "data/products.csv"
SALES = "data/sales.csv"


def main():
    pd.set_option("display.max_rows", 1000)
    revenueGrowth()
    bestDay()
    bestDayOfProduct("Banana")
    bestSellingProduct()
    productSalesByTime()
    bestProductRevenue()


def revenueGrowth():
    df = pd.read_csv(SALES, parse_dates=["DATA"])
    df.set_index("DATA", inplace=True)

    monthlyRevenue = df.resample("ME")[["VALOR_VENDA"]].sum()
    august = monthlyRevenue.values[0][0]
    september = monthlyRevenue.values[1][0]
    october = monthlyRevenue.values[2][0]
    septemberGrowth = (september - august) / august * 100
    octoberGrowth = (october - september) / september * 100
    print("---------------------Q1---------------------")
    print("Faturamento em Ago: R$ " + "{:.2f}".format(august))
    print("Faturamento em Set: R$ " + "{:.2f}".format(september))
    print("Faturamento em Out: R$ " + "{:.2f}".format(october))
    print("Crescimento mensal em 09/21: " + "{:.2f}".format(septemberGrowth) + "%")
    print("Crescimento mensal em 10/21: " + "{:.2f}".format(octoberGrowth) + "%")
    print("--------------------------------------------\n")

    plt.figure(figsize=(16, 9))
    plt.bar(monthlyRevenue.index, monthlyRevenue["VALOR_VENDA"], color='green', label=monthlyRevenue.index, width=0.8)
    plt.title('Faturamento mensal')
    plt.xlabel('Data')
    plt.ylabel('Faturamento (R$)')
    plt.grid(True, axis="y")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # plt.show()
    plt.savefig("graphs/monthly_revenue.png")


def bestDay():
    df = pd.read_csv(SALES, parse_dates=["DATA"])

    dailyRevenue = df[["DATA", "VALOR_VENDA"]].groupby("DATA", sort=False)[["VALOR_VENDA"]].sum()
    day = dailyRevenue.idxmax().values[0]
    bestDayTotal = dailyRevenue.max().values[0]

    print("---------------------Q2---------------------")
    print(f"Melhor dia em vendas: {day}")
    print("Faturamento: R$ " + "{:.2f}".format(bestDayTotal))
    print("--------------------------------------------\n")

    plt.figure(figsize=(16, 9))
    plt.bar(dailyRevenue.index, dailyRevenue["VALOR_VENDA"], color='green', label=dailyRevenue.index, width=0.8)
    plt.title('Faturamento diário')
    plt.xlabel('Data')
    plt.ylabel('Faturamento (R$)')
    plt.grid(True, axis="y")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # plt.show()
    plt.savefig("graphs/best_day.png")


def bestDayOfProduct(product):
    products = populateProductsDict()
    productId = int(products[product]["ID_PRODUTO"])

    df = pd.read_csv(SALES, parse_dates=["DATA"])

    dailyRevenue = df[["DATA", "VALOR_VENDA", "ID_PRODUTO"]].query(
        "ID_PRODUTO == @productId").groupby(
            "DATA", sort=False)[["VALOR_VENDA"]].sum()
    bestDayTotal = dailyRevenue.max().values[0]
    bestDay = dailyRevenue.idxmax().values[0]

    print("---------------------Q3---------------------")
    print(f"Melhor dia de {product}: {bestDay}")
    print("Total: R$ " + "{:.2f}".format(bestDayTotal))
    print("--------------------------------------------\n")

    plt.figure(figsize=(16, 9))
    plt.bar(dailyRevenue.index, dailyRevenue["VALOR_VENDA"], color='green', label=dailyRevenue.index, width=0.8)
    plt.title(f'Faturamento diário de {product}')
    plt.xlabel('Data')
    plt.ylabel('Faturamento (R$)')
    plt.grid(True, axis="y")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # plt.show()
    plt.savefig(f"graphs/daily_{product}_revenue.png")


def bestSellingProduct():
    products = populateProductsDict("id")
    df = pd.read_csv(SALES)
    revenueByProduct = df[["VALOR_VENDA", "ID_PRODUTO"]].groupby("ID_PRODUTO")[["VALOR_VENDA"]].sum()

    pricesPerKg = []
    for item in revenueByProduct.index.array:
        pricesPerKg.append(float(products[item]["PREÇO_KG"]))
    pricesPerKg = pd.Series(data=pricesPerKg, copy=False)
    pricesPerKg.index = pricesPerKg.index + 1
    kgsByProduct = revenueByProduct.div(pricesPerKg, axis=0)

    revenueByProduct.index = revenueByProduct.index.map(lambda x: products[x]["NOME_PRODUTO"])
    revenueByProduct.index.name = "NOME_PRODUTO"

    kgsByProduct.index = kgsByProduct.index.map(lambda x: products[x]["NOME_PRODUTO"])
    kgsByProduct.index.name = "NOME_PRODUTO"

    bestSellerKgs = kgsByProduct.max().values[0]
    bestSeller = kgsByProduct.idxmax().values[0]
    print("---------------------Q4---------------------")
    print(f"Produto mais vendido: {bestSeller}")
    print(f"Quantidade vendida: {bestSellerKgs} Kgs")
    print("--------------------------------------------\n")

    figure, axis = plt.subplots(1, 2)
    axis[0].set_title(f'Vendas totais por produto')
    axis[0].bar(kgsByProduct.index, kgsByProduct["VALOR_VENDA"], color='green', label=kgsByProduct.index, width=0.8)
    axis[0].bar(kgsByProduct.index, kgsByProduct["VALOR_VENDA"], color='green', label=kgsByProduct.index, width=0.8)
    axis[0].set_xlabel('Produto')
    axis[0].set_ylabel('Vendas (Kg)')
    axis[0].grid(True, axis="y")
    axis[0].tick_params(axis='x', rotation=90)

    axis[1].set_title(f'Porcentagem de cada produto')
    axis[1].pie(kgsByProduct["VALOR_VENDA"], labels=kgsByProduct.index)

    plt.tight_layout()
    # plt.show()
    plt.savefig("graphs/products_sales_kgs.png")


def bestProductRevenue():
    products = populateProductsDict("id")
    df = pd.read_csv(SALES)
    revenueByProduct = df[["VALOR_VENDA", "ID_PRODUTO"]].groupby("ID_PRODUTO")[["VALOR_VENDA"]].sum()

    revenueByProduct.index = revenueByProduct.index.map(lambda x: products[x]["NOME_PRODUTO"])
    revenueByProduct.index.name = "NOME_PRODUTO"

    figure, axis = plt.subplots(1, 2)
    axis[0].set_title(f'Vendas totais por produto')
    axis[0].bar(revenueByProduct.index, revenueByProduct["VALOR_VENDA"], color='green', label=revenueByProduct.index, width=0.8)
    axis[0].bar(revenueByProduct.index, revenueByProduct["VALOR_VENDA"], color='green', label=revenueByProduct.index, width=0.8)
    axis[0].set_xlabel('Produto')
    axis[0].set_ylabel('Vendas (R$)')
    axis[0].grid(True, axis="y")
    axis[0].tick_params(axis='x', rotation=90)

    axis[1].set_title(f'Porcentagem de cada produto')
    axis[1].pie(revenueByProduct["VALOR_VENDA"], labels=revenueByProduct.index)

    plt.tight_layout()
    plt.savefig("graphs/revenue_by_product.png")


def productSalesByTime(product="all"):
    products = populateProductsDict()
    if product != "all":
        productId = int(products[product]["ID_PRODUTO"])

    df = pd.read_csv(SALES, parse_dates=["FAIXA_HORARIO"])
    df["FAIXA_HORARIO"] = df["FAIXA_HORARIO"].dt.strftime("%H:%M")
    print(df[["FAIXA_HORARIO"]])

    if product == "all":
        dailyRevenue = df[["DATA", "VALOR_VENDA", "ID_PRODUTO", "FAIXA_HORARIO"]].groupby(
            "FAIXA_HORARIO", sort=True)[["VALOR_VENDA"]].sum()
    else:
        dailyRevenue = df[["DATA", "VALOR_VENDA", "ID_PRODUTO", "FAIXA_HORARIO"]].query(
            "ID_PRODUTO == @productId").groupby(
                "FAIXA_HORARIO", sort=True)[["VALOR_VENDA"]].sum()

    plt.figure(figsize=(16, 9))
    plt.bar(dailyRevenue.index, dailyRevenue["VALOR_VENDA"], color='green', label=dailyRevenue.index, width=0.8)
    if product == "all":
        plt.title('Faturamento por hora')
    else:
        plt.title(f'Faturamento por hora com {product}')
    plt.xlabel("Hora")
    plt.ylabel('Faturamento (R$)')
    plt.grid(True, axis="y")
    plt.xticks(rotation=90)
    plt.tight_layout()


def populateProductsDict(key="name"):
    with open('./data/products.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        productsDict = {}
        for lines in csvFile:
            if key == "name":
                productsDict[lines["NOME_PRODUTO"]] = lines
            elif key == "id":
                productsDict[int(lines["ID_PRODUTO"])] = lines
    return productsDict


if __name__ == "__main__":
    main()
