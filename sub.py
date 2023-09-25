import socket
import requests
from colorama import Fore, Style

def download_subdomain_list(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"Erro ao baixar a lista de subdomínios. Código de status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a solicitação HTTP: {e}")
    return []

def enum_subdomains(domain, subdomain_list):
    existing_subdomains = []

    for subdomain in subdomain_list:
        full_domain = f"{subdomain}.{domain}"
        try:
            # Tentar resolver o subdomínio
            socket.gethostbyname(full_domain)
            existing_subdomains.append(full_domain)
        except socket.gaierror as e:
            print(f"Erro ao resolver o subdomínio {full_domain}: {e}")

    return existing_subdomains

if __name__ == "__main__":
    domain = input("Digite o domínio principal (exemplo.com): ")
    subdomain_list_url = "https://raw.githubusercontent.com/rbsec/dnscan/master/subdomains-10000.txt"
    subdomain_list = download_subdomain_list(subdomain_list_url)

    if subdomain_list:
        subdomains = enum_subdomains(domain, subdomain_list)

        if subdomains:
            print("Subdomínios encontrados:")
            for subdomain in subdomains:
                print(Fore.GREEN + subdomain + Style.RESET_ALL)
        else:
            print("Nenhum subdomínio encontrado.")
    else:
        print("A lista de subdomínios não pôde ser baixada.")
