import socket
import requests
import subprocess
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def check_ports(host, ports=(80, 8080, 443, 3000, 5000), timeout=1.0):
    results = {}
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            results[port] = True
        except Exception:
            results[port] = False
        finally:
            s.close()
    return results


def probe_http(host, port):
    if port == 443:
        url = f"https://{host}"
    else:
        url = f"http://{host}:{port}"

    try:
        response = requests.get(url, timeout=3)
        return {
            "port": port,
            "url": url,
            "status_code": response.status_code,
            "reason": response.reason
        }
    except requests.exceptions.RequestException as e:
        return {
            "port": port,
            "url": url,
            "status_code": None,
            "reason": str(e)
        }




def check_ssl(host, port=443):
    try:
        result = subprocess.run(
            ["openssl", "s_client", "-connect", f"{host}:{port}", "-servername", host, "-showcerts"],
            capture_output=True,
            text=True,
            input="",
            timeout=10
        )
        output = result.stdout

        certs = []
        current_cert = []
        in_cert = False

        for line in output.splitlines():
            if "-----BEGIN CERTIFICATE-----" in line:
                in_cert = True
                current_cert = [line]
            elif "-----END CERTIFICATE-----" in line:
                current_cert.append(line)
                certs.append("\n".join(current_cert))
                in_cert = False
            elif in_cert:
                current_cert.append(line)

        if not certs:
            return {"error": "No certificate found"}

        leaf_cert = x509.load_pem_x509_certificate(certs[0].encode(), default_backend())

        info = {
            "subject": leaf_cert.subject.rfc4514_string(),
            "issuer": leaf_cert.issuer.rfc4514_string(),
            "valid_from": leaf_cert.not_valid_before_utc,
            "valid_to": leaf_cert.not_valid_after_utc,
            "pem": certs
        }

        return info

    except Exception as e:
        return {"error": str(e)}





def run_whatweb(url):      #### WHATWEB ####
    """
    Runs whatweb against the given URL and returns the output.
    """
    try:
        result = subprocess.run(
            ["whatweb", url],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running whatweb: {e}"



def show_summary(results):       #### #OUTPUT ###
    ok_sites = []

    for res in results:
        print("+" * 50)
        print("                 - Valid Request -                 ")
        #print("-" * 50)
        print(f"Port: {res['port']}")
        print(f"URL: {res['url']}")
        print(f"Status: {res['status_code']} {res['reason']}")
        print("-" * 50)

        if res.get("ssl_subject"):
            print(f"SSL Subject: {res['ssl_subject']}")
            print(f"SSL Issuer: {res['ssl_issuer']}")
            print(f"Valid From: {res['ssl_valid_from']}")
            print(f"Valid To: {res['ssl_valid_to']}")
            print("-" * 50)

        if res.get("whatweb"):
            print(f"WhatWeb: {res['whatweb']}")

        if res['status_code'] == 200:
            ok_sites.append(res['url'])

    print("-" * 50)
    print("+" * 50)
    return ok_sites




def main():
    host = input("Input IP address or hostname: ").strip()
    choice = int(input("Select what webs to check:\n1 - HTTP\n2 - HTTPS\n3 - Both\n> "))
    print("This might take a minute...")

    ports = []
    if choice == 1:
        ports = [80, 8080]
    elif choice == 2:
        ports = [443]
    elif choice == 3:
        ports = [80, 8080, 443]

    open_ports = check_ports(host, ports)

    results = []
    for port, is_open in open_ports.items():
        if is_open:
            probe_result = probe_http(host, port)

            # SSL
            if port == 443:
                ssl_info = check_ssl(host)
                if "error" not in ssl_info:
                    probe_result["ssl_subject"] = ssl_info["subject"]
                    probe_result["ssl_issuer"] = ssl_info["issuer"]
                    probe_result["ssl_valid_from"] = ssl_info["valid_from"]
                    probe_result["ssl_valid_to"] = ssl_info["valid_to"]
                    probe_result["ssl_pem"] = ssl_info["pem"]
                else:
                    probe_result["ssl_subject"] = probe_result["ssl_issuer"] = "Error"
                    probe_result["ssl_valid_from"] = probe_result["ssl_valid_to"] = ssl_info.get("error")
                    probe_result["ssl_pem"] = None

            # WhatWeb
            if probe_result["status_code"] == 200:
                probe_result["whatweb"] = run_whatweb(probe_result["url"])
            else:
                probe_result["whatweb"] = None

            results.append(probe_result)

    ok_sites = show_summary(results)

if __name__ == "__main__":
    main()
