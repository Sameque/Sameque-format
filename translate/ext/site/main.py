from flask import Blueprint, render_template, request
from translate.ext.format.edi import to_sql

bp = Blueprint("site", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/edi", methods=["GET", "POST"])
def edi():
    title = "EDI"
    if request.method == "POST":

        conteudo = to_sql(request.form["content"])
        return render_template("edi/index.html", title=title, content=conteudo)

    else:
        return render_template("edi/index.html", title=title)
