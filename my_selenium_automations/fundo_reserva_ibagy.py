#!/usr/bin/env python

import argparse
import re
import sys
import tomllib
from pathlib import Path

import pypdf

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


FUNDO_RE = re.compile(r"Fundo de Reserva\D*?(?P<fundo>\d+(,?\d{2}))")

DEFAULT_CONFIG_PATH = (
    Path.home() / ".config" / "my-selenium-automations" / "config.toml"
)

IBAGY_FUNDO_RESERVA_KEY = "ibagy-fundo-reserva"

# REDIRECT_URL = "https://ibagy.com.br/obrigado/?target=fundo-de-reserva"
REDIRECT_URL_RE = r"ibagy\.com\.br/obrigado"

TIMEOUT = 30
IMPLICIT_TIMEOUT = 5


# ATENCAO: Use a ferramenta selenium-manager para automaticamente gerenciar os webdrivers
# está instalada em $VIRTUAL_ENV/lib/python3.11/site-packages/selenium/webdriver/common/linux/selenium-manager
# https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-selenium-manager-beta


def _parsear_fundo_de_reserva(pdf_filepath):
    with open(pdf_filepath, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if m := FUNDO_RE.search(page_text):
                return m.group("fundo")

    return None


def _submit_ibagy_form(
    *, fundo_valor, file_a, file_b, full_name, email, telephone, contract_number
):
    with webdriver.Chrome() as driver:
        # navigate to the URL
        driver.get("https://ibagy.com.br/area-do-cliente/")
        driver.implicitly_wait(3)
        # fundo_reservas_access_btn = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="a[href='#clb-modal-areadocliente-bloco1']"))

        cookies_btn = driver.find_element(by=By.ID, value="cookie-consent-btn")
        cookies_btn.click()

        fundo_reservas_access_btn = driver.find_element(
            by=By.CSS_SELECTOR, value="a[href='#clb-modal-areadocliente-bloco1']"
        )
        fundo_reservas_access_btn.click()

        # nome_inquilino_input = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element(by=By.CSS_SELECTOR, value="input[name='nome_do_inquilino']"))
        nome_inquilino_input = driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='nome_do_inquilino']"
        )
        nome_inquilino_input.send_keys(full_name)

        email_input = driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='email']"
        )
        email_input.send_keys(email)

        telefone_input = driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='telefone']"
        )
        telefone_input.send_keys(telephone)

        codigo_contrato = driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='codigo_do_contrato']"
        )
        codigo_contrato.send_keys(contract_number)

        observacoes_input = driver.find_element(
            by=By.CSS_SELECTOR, value="textarea[name='observacoes']"
        )
        observacoes_input.send_keys(f"Fundo de reserva: {fundo_valor}")

        anexos_input = driver.find_element(
            by=By.CSS_SELECTOR, value="input.dz-hidden-input[type='file']"
        )
        anexos_input.send_keys("\n".join([str(file_a), str(file_b)]))

        accept_termos = driver.find_element(by=By.CSS_SELECTOR, value="div.checkmark")
        accept_termos.click()

        enviar_btn = driver.find_element(by=By.ID, value="FORM_A_submit-action-button")
        enviar_btn.click()

        WebDriverWait(driver, timeout=TIMEOUT).until(EC.url_matches(REDIRECT_URL_RE))
        # time.sleep(TIMEOUT)


def _to_absolute_path(arg):
    return Path(arg).absolute()


parser = argparse.ArgumentParser()
parser.add_argument("file_a", type=_to_absolute_path)
parser.add_argument("file_b", type=_to_absolute_path)
parser.add_argument("-c", "--config-file")
parser.add_argument("-r", "--fundo-reserva-valor")


def main():
    args = parser.parse_args()
    config_file = args.config_file or DEFAULT_CONFIG_PATH
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    ibagy_data = data[IBAGY_FUNDO_RESERVA_KEY]

    fundo_valor = args.fundo_reserva_valor
    if fundo_valor is None:
        fundo_valor = _parsear_fundo_de_reserva(
            args.file_a
        ) or _parsear_fundo_de_reserva(args.file_b)

    if fundo_valor is None:
        print("Não foi possível achar valor de reserva")
        sys.exit(1)

    print(f"Fundo de reserva: {fundo_valor}")
    _submit_ibagy_form(
        fundo_valor=fundo_valor, file_a=args.file_a, file_b=args.file_b, **ibagy_data
    )


if __name__ == "__main__":
    main()
