import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import uuid
import io
import os
import streamlit.components.v1 as components

# --- CONFIGURACIÓN BASE DE DATOS ---
DB_NAME = "ilusion_v14.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventario 
                          (producto TEXT, modelo TEXT, color TEXT, talla TEXT, 
                           stock INTEGER, p_compra REAL, p_venta REAL, imagen TEXT,
                           PRIMARY KEY (producto, modelo, color, talla))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ventas 
                          (transaccion_id TEXT, fecha TEXT, hora TEXT, producto TEXT, modelo TEXT, 
                           color TEXT, talla TEXT, cantidad INTEGER, p_venta REAL, total REAL, estado TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS apartados 
                          (id TEXT, cliente TEXT, fecha TEXT, producto TEXT, modelo TEXT, 
                           color TEXT, talla TEXT, cantidad INTEGER, estado TEXT)''')
        conn.commit()

    # --- INSERCIÓN AUTOMÁTICA DE LOS 400 REGISTROS (ESCOLAR) ---
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Verificamos si la tabla ya tiene datos para no duplicar cada vez que cargues la página
            cursor.execute("SELECT COUNT(*) FROM inventario")
            total = cursor.fetchone()[0]
            
            if total == 0:
                # Aquí están incrustados los 400 registros escolares generados dinámicamente
                nuevos_registros = [
                    ('Playera', 'MOD-1', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-2', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-3', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-4', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-5', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-6', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-7', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-8', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-9', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-10', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-11', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-12', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-13', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-14', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-15', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-16', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-17', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-18', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-19', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-20', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-21', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-22', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-23', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-24', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-25', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-26', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-27', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-28', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-29', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-30', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-31', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-32', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-33', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-34', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-35', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-36', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-37', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-38', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-39', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-40', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-41', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-42', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-43', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-44', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-45', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-46', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-47', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-48', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-49', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-50', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-51', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-52', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-53', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-54', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-55', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-56', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-57', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-58', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-59', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-60', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-61', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-62', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-63', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-64', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-65', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-66', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-67', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-68', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-69', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-70', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-71', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-72', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-73', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-74', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-75', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-76', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-77', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-78', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-79', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-80', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-81', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-82', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-83', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-44', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-85', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-86', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-87', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-88', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-89', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-90', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-91', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-92', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-93', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-94', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-95', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-96', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-97', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-98', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-99', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-100', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-101', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-102', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-103', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-104', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-105', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-106', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-107', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-108', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-109', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-110', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-111', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-112', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-113', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-114', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-115', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-116', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-117', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-118', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-119', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-120', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-121', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-122', 'Blanco', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-123', 'Azul', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-124', 'Rojo', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-125', 'Rosa', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-126', 'Gris', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-127', 'Verde', 'G', 15, 150.0, 225.0, ''),  
                    ('Lencería', 'MOD-128', 'Beige', 'XG', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-129', 'Morado', 'CH', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-130', 'Café', 'M', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-131', 'Negro', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-132', 'Blanco', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-133', 'Azul', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-134', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-135', 'Rosa', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-136', 'Gris', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-137', 'Verde', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-138', 'Beige', 'M', 15, 175.0, 262.5, ''),
                    ('Short', 'MOD-139', 'Morado', 'G', 15, 200.0, 300.0, ''),
                    ('Pantalón', 'MOD-140', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Playera', 'MOD-141', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-142', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-143', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-144', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-145', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-146', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-147', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-148', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-149', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-150', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-151', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-152', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-153', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-154', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-155', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-156', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-157', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-158', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-159', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-160', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-161', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-162', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-163', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-164', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-165', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-166', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-167', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-168', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-169', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-170', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-171', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-172', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-173', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-174', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-175', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Blusa', 'MOD-176', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Blusa', 'MOD-177', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Blusa', 'MOD-178', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Blusa', 'MOD-179', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Blusa', 'MOD-180', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-181', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-182', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-183', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-184', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-185', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-186', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-187', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-188', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-189', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-190', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-191', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-192', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-193', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-194', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-195', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-196', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-197', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-198', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-199', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-200', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-201', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-202', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-203', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-204', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-205', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-206', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-207', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-208', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-209', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-210', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-211', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-212', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-213', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-214', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-215', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Jeans', 'MOD-216', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Jeans', 'MOD-217', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Jeans', 'MOD-218', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Jeans', 'MOD-219', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Jeans', 'MOD-220', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-221', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-222', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-223', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-224', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-225', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-226', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-227', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-228', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-229', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-230', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-231', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-232', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-233', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-234', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-235', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-236', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-237', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-238', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-239', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-240', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-241', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-242', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-243', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-244', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-245', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-246', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-247', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-248', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-249', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-250', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-251', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-252', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-253', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-254', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-255', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Vestido', 'MOD-256', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Vestido', 'MOD-257', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Vestido', 'MOD-258', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Vestido', 'MOD-259', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Vestido', 'MOD-260', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-261', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-262', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-263', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-264', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-265', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-266', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-267', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-268', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-269', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-270', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-271', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-272', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-273', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-274', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-275', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-276', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-277', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-278', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-279', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-280', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-281', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-282', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-283', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-284', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-285', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-286', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-287', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-288', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-289', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-290', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-291', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-292', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-293', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-294', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-295', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Falda', 'MOD-296', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Falda', 'MOD-297', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Falda', 'MOD-298', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Falda', 'MOD-299', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Falda', 'MOD-300', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-301', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-302', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-303', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-304', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-305', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-306', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-307', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-308', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-309', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-310', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-311', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-312', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-313', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-314', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-315', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-316', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-317', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-318', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-319', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-320', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-321', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-322', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-323', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-324', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-325', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-326', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-327', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-328', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-329', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-330', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-331', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-332', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-333', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-334', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-335', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Sudadera', 'MOD-336', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Sudadera', 'MOD-337', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Sudadera', 'MOD-338', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Sudadera', 'MOD-339', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Sudadera', 'MOD-340', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-341', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-342', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-343', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-344', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-345', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-346', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-347', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-348', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-349', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-350', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-351', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-352', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-353', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-354', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-355', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-356', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-357', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-358', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-359', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-360', 'Rosa', 'XG', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-361', 'Gris', 'CH', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-362', 'Gris', 'M', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-363', 'Gris', 'G', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-364', 'Gris', 'XG', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-365', 'Verde', 'CH', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-366', 'Verde', 'M', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-367', 'Verde', 'G', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-368', 'Verde', 'XG', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-369', 'Beige', 'CH', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-370', 'Beige', 'M', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-371', 'Beige', 'G', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-372', 'Beige', 'XG', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-373', 'Morado', 'CH', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-374', 'Morado', 'M', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-375', 'Morado', 'G', 15, 100.0, 150.0, ''),
                    ('Suéter', 'MOD-376', 'Morado', 'XG', 15, 125.0, 187.5, ''),
                    ('Suéter', 'MOD-377', 'Café', 'CH', 15, 150.0, 225.0, ''),
                    ('Suéter', 'MOD-378', 'Café', 'M', 15, 175.0, 262.5, ''),
                    ('Suéter', 'MOD-379', 'Café', 'G', 15, 200.0, 300.0, ''),
                    ('Suéter', 'MOD-380', 'Café', 'XG', 15, 100.0, 150.0, ''),
                    ('Lencería', 'MOD-381', 'Negro', 'CH', 15, 125.0, 187.5, ''),
                    ('Lencería', 'MOD-382', 'Negro', 'M', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-383', 'Negro', 'G', 15, 175.0, 262.5, ''),
                    ('Lencería', 'MOD-384', 'Negro', 'XG', 15, 200.0, 300.0, ''),
                    ('Lencería', 'MOD-385', 'Blanco', 'CH', 15, 100.0, 150.0, ''),
                    ('Lencería', 'MOD-386', 'Blanco', 'M', 15, 125.0, 187.5, ''),
                    ('Lencería', 'MOD-387', 'Blanco', 'G', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-388', 'Blanco', 'XG', 15, 175.0, 262.5, ''),
                    ('Lencería', 'MOD-389', 'Azul', 'CH', 15, 200.0, 300.0, ''),
                    ('Lencería', 'MOD-390', 'Azul', 'M', 15, 100.0, 150.0, ''),
                    ('Lencería', 'MOD-391', 'Azul', 'G', 15, 125.0, 187.5, ''),
                    ('Lencería', 'MOD-392', 'Azul', 'XG', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-393', 'Rojo', 'CH', 15, 175.0, 262.5, ''),
                    ('Lencería', 'MOD-394', 'Rojo', 'M', 15, 200.0, 300.0, ''),
                    ('Lencería', 'MOD-395', 'Rojo', 'G', 15, 100.0, 150.0, ''),
                    ('Lencería', 'MOD-396', 'Rojo', 'XG', 15, 125.0, 187.5, ''),
                    ('Lencería', 'MOD-397', 'Rosa', 'CH', 15, 150.0, 225.0, ''),
                    ('Lencería', 'MOD-398', 'Rosa', 'M', 15, 175.0, 262.5, ''),
                    ('Lencería', 'MOD-399', 'Rosa', 'G', 15, 200.0, 300.0, ''),
                    ('Lencería', 'MOD-400', 'Rosa', 'XG', 15, 100.0, 150.0, '')
]
                cursor.executemany("INSERT OR REPLACE INTO inventario VALUES (?, ?, ?, ?, ?, ?, ?, ?)", nuevos_registros)
                conn.commit()
    except Exception as e:
        st.error(f"Error al cargar datos escolares: {e}")

def run_query(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def get_df(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query(query, conn, params=params)

# --- FUNCIÓN DE IMPRESIÓN ---
def ejecutar_impresion(html_content):
    unique_id = str(uuid.uuid4())[:8]
    component_script = f"""
    <div id="ticket-{unique_id}" style="display:none;">{html_content}</div>
    <script>
        (function() {{
            var content = document.getElementById('ticket-{unique_id}').innerHTML;
            var win = window.open('', 'PRINT', 'height=600,width=400');
            win.document.write('<html><head><title>Imprimir</title></head><body>' + content + '</body></html>');
            win.document.close();
            win.focus();
            win.print();
            win.close();
        }})();
    </script>
    """
    components.html(component_script, height=0)

def generar_ticket_html(titulo, id_doc, items, total, cliente=None):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""
    <div style="font-family: 'Courier New', monospace; width: 250px; padding: 10px; background: white; color: black; border: 1px solid #ddd;">
        <center><h2 style="margin:0;">ILUSIÓN</h2><p style="font-size:12px; margin:0;">Punto de Venta</p></center>
        <hr>
        <p style="font-size:11px;"><b>{titulo}</b>: #{id_doc}<br><b>Fecha:</b> {fecha}</p>
        {f'<p style="font-size:11px;"><b>Cliente:</b> {cliente}</p>' if cliente else ''}
        <table style="width:100%; font-size:10px;">
            {"".join([f"<tr><td>{it['modelo']}</td><td align='center'>{it['cantidad']}</td><td align='right'>${it['subtotal']:,.2f}</td></tr>" for it in items])}
        </table>
        <hr><h3 align="right">TOTAL: ${total:,.2f}</h3>
    </div>
    """

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="Ilusion Pro V14", layout="wide")
init_db()

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'ticket_a_imprimir' not in st.session_state: st.session_state.ticket_a_imprimir = None

# --- NAVEGACIÓN ---
st.sidebar.title("SISTEMA ILUSION")
menu = ["📦 Inventario", "🛒 Punto de Venta", "📝 Apartados", "📊 Corte de Caja", "📉 Historial", "🛠 Admin", "💾 Respaldos"]
choice = st.sidebar.selectbox("Opciones", menu)

if st.session_state.ticket_a_imprimir:
    ejecutar_impresion(st.session_state.ticket_a_imprimir)
    st.session_state.ticket_a_imprimir = None

# --- 1. INVENTARIO ---
if choice == "📦 Inventario":
    st.header("Inventario de Prendas")
    st.dataframe(get_df("SELECT * FROM inventario"), width='stretch')

# --- 2. PUNTO DE VENTA (CON BOTÓN LIMPIAR) ---
elif choice == "🛒 Punto de Venta":
    st.header("Nueva Operación")
    df_inv = get_df("SELECT * FROM inventario WHERE stock > 0")
    
    if not df_inv.empty:
        c1, c2 = st.columns(2)
        with c1:
            mod_sel = st.selectbox("Modelo", sorted(df_inv['modelo'].unique()))
            df_f = df_inv[df_inv['modelo'] == mod_sel]
            col_sel = st.selectbox("Color", sorted(df_f['color'].unique()))
            df_f = df_f[df_f['color'] == col_sel]
            talla_sel = st.selectbox("Talla", sorted(df_f['talla'].unique()))
            item = df_f[df_f['talla'] == talla_sel].iloc[0]
            
            st.info(f"Stock: {item['stock']} | Precio: ${item['p_venta']:,.2f}")
            cant = st.number_input("Cantidad", 1, int(item['stock']))
            
            if st.button("➕ Agregar al Carrito", use_container_width=True):
                st.session_state.carrito.append({
                    'producto': item['producto'], 'modelo': item['modelo'], 'color': item['color'],
                    'talla': item['talla'], 'cantidad': cant, 'precio': item['p_venta'], 'subtotal': item['p_venta']*cant
                })
                st.rerun()
            
            # BOTÓN LIMPIAR CAMPOS / CARRITO
            if st.button("🗑️ Limpiar Todo", type="secondary", use_container_width=True):
                st.session_state.carrito = []
                st.rerun()

        with c2:
            if st.session_state.carrito:
                st.subheader("Resumen de Venta")
                st.table(pd.DataFrame(st.session_state.carrito)[['modelo', 'talla', 'cantidad', 'subtotal']])
                total_v = sum(i['subtotal'] for i in st.session_state.carrito)
                if st.button(f"✅ Finalizar e Imprimir (${total_v:,.2f})", type="primary", use_container_width=True):
                    t_id = str(uuid.uuid4())[:8].upper()
                    now = datetime.now()
                    for i in st.session_state.carrito:
                        run_query("INSERT INTO ventas VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                                  (t_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), i['producto'], i['modelo'], i['color'], i['talla'], i['cantidad'], i['precio'], i['subtotal'], "COMPLETADA"))
                        run_query("UPDATE inventario SET stock = stock - ? WHERE modelo=? AND color=? AND talla=?", (i['cantidad'], i['modelo'], i['color'], i['talla']))
                    st.session_state.ticket_a_imprimir = generar_ticket_html("TICKET VENTA", t_id, st.session_state.carrito, total_v)
                    st.session_state.carrito = []
                    st.rerun()

# --- 3. APARTADOS ---
elif choice == "📝 Apartados":
    st.header("Control de Apartados")
    df_inv = get_df("SELECT * FROM inventario WHERE stock > 0")
    if not df_inv.empty:
        with st.form("ap_f"):
            cli = st.text_input("Nombre de la Clienta")
            df_inv['lbl'] = df_inv['modelo'] + " | " + df_inv['color'] + " (" + df_inv['talla'] + ")"
            sel = st.selectbox("Prenda", df_inv['lbl'] if not df_inv.empty else ["Vacío"])
            cnt = st.number_input("Cant", 1)
            if st.form_submit_button("Guardar Apartado"):
                r = df_inv[df_inv['lbl'] == sel].iloc[0]
                ap_id = "AP-" + str(uuid.uuid4())[:4].upper()
                run_query("INSERT INTO apartados VALUES (?,?,?,?,?,?,?,?,?)", (ap_id, cli, datetime.now().strftime("%Y-%m-%d"), r['producto'], r['modelo'], r['color'], r['talla'], cnt, "ACTIVO"))
                run_query("UPDATE inventario SET stock = stock - ? WHERE modelo=? AND color=? AND talla=?", (cnt, r['modelo'], r['color'], r['talla']))
                st.session_state.ticket_a_imprimir = generar_ticket_html("VALE APARTADO", ap_id, [{'modelo': r['modelo'], 'cantidad': cnt, 'subtotal': r['p_venta']*cnt}], r['p_venta']*cnt, cliente=cli)
                st.rerun()
    else:
        st.info("No hay inventario disponible para apartar.")

# --- 4. CORTE DE CAJA ---
elif choice == "📊 Corte de Caja":
    st.header("Corte de Caja y Utilidades")
    periodo = st.radio("Seleccione Periodo de Corte:", ["Hoy", "Esta Semana", "Este Mes"], horizontal=True)
    
    hoy = datetime.now()
    if periodo == "Hoy":
        fecha_inicio = hoy.strftime("%Y-%m-%d")
    elif periodo == "Esta Semana":
        fecha_inicio = (hoy - timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
    else:
        fecha_inicio = hoy.strftime("%Y-%m-01")
    
    query_corte = """
        SELECT v.*, i.p_compra 
        FROM ventas v 
        LEFT JOIN inventario i ON v.modelo = i.modelo AND v.color = i.color AND v.talla = i.talla
        WHERE v.fecha >= ? AND v.estado = 'COMPLETADA'
    """
    df_corte = get_df(query_corte, (fecha_inicio,))
    
    if not df_corte.empty:
        total_ventas = df_corte['total'].sum()
        total_costos = (df_corte['cantidad'] * df_corte['p_compra']).sum()
        utilidad = total_ventas - total_costos
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Ingresos Totales", f"${total_ventas:,.2f}")
        m2.metric("Inversión (Costos)", f"${total_costos:,.2f}")
        m3.metric("Utilidad Neta", f"${utilidad:,.2f}", delta=f"{ (utilidad/total_ventas)*100:.1f}%" if total_ventas > 0 else "0%")
        
        st.subheader("Detalle de Ventas en el Periodo")
        st.dataframe(df_corte[['transaccion_id', 'fecha', 'modelo', 'talla', 'cantidad', 'total']], width='stretch')
    else:
        st.info(f"No hay ventas registradas desde el {fecha_inicio}")

# --- 5. HISTORIAL ---
elif choice == "📉 Historial":
    st.header("Historial de Operaciones")
    st.subheader("Ventas")
    st.dataframe(get_df("SELECT * FROM ventas"), width='stretch')
    st.subheader("Apartados")
    st.dataframe(get_df("SELECT * FROM apartados"), width='stretch')

# --- 6. ADMIN ---
elif choice == "🛠 Admin":
    with st.form("adm"):
        c1, c2, c3, c4 = st.columns(4)
        p, m, col, t = c1.text_input("Art"), c2.text_input("Mod"), c3.text_input("Col"), c4.text_input("Tal")
        s = st.number_input("Stock", 0)
        pc, pv = st.number_input("Costo", 0.0), st.number_input("Venta", 0.0)
        if st.form_submit_button("Guardar en Inventario"):
            run_query("INSERT OR REPLACE INTO inventario VALUES (?,?,?,?,?,?,?,?)", (p,m,col,t,s,pc,pv,""))
            st.success("Guardado.")

# --- 7. RESPALDOS ---
elif choice == "💾 Respaldos":
    st.header("Respaldos")
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as f:
            st.download_button("📥 Descargar DB", f, f"Backup_Ilusion_{datetime.now().strftime('%Y%m%d')}.db")
    
    file_up = st.file_uploader("Restaurar", type=["db"])
    if file_up and st.button("🚀 Restaurar"):
        with open(DB_NAME, "wb") as f: f.write(file_up.getbuffer())
        st.rerun()