# Federal Institute of Education, Science and Technology
# of State of Santa Catarina.
#
# Copyright (c) 2026 Pagani from IFSC Xanxerê. All rights reserved.
#
# This file was published under the AGPL-3.0-only license, 
# You can read it from "LICESE" file in the repository root.
#
# (filename:functions.py)
# (project_code:gesture-recon-py)
# (project_name:"Reconhecimento de Gestos com Python")
# (scope:"Projeto Avaliativo Trimestral para a disciplina 'Tópicos Avançados em Informática'")


from requests import request
from requests.exceptions import RequestException


def ping_http(addr: str) -> bool:
  try:
    rs = request(url=addr, method="GET")
    return rs.ok
  except RequestException:
    return False
