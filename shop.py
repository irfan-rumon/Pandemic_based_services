from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from userDB import UserGeneralDb
shop = Blueprint("shop",__name__, static_folder="static", template_folder="templates")