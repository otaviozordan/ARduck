#https://blog.devgenius.io/chatgpt-how-to-use-it-with-python-5d729ac34c0d -> Tutorial

from app import app, db
from app.models.questoes_table import Questoes, verificarRespostaCorreta
from flask import Response, request
import json