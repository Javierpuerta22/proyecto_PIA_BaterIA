import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager


# Initialize APP
app = Flask(__name__, template_folder='../templates', static_folder="../static")
CORS(app)
jwt = JWTManager(app)

