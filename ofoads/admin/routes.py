from flask import render_template

from . import admin

@admin.route('/login')
def login():
    return render_template('admin/login.html')