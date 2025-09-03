import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Agencia de Viajes",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Datos de ejemplo
def cargar_datos():
    # Clientes
    clientes_data = {
        'id': [1, 2, 3, 4, 5],
        'nombre': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez'],
        'email': ['ana@email.com', 'carlos@email.com', 'maria@email.com', 'juan@email.com', 'laura@email.com'],
        'telefono': ['123456789', '987654321', '456789123', '321654987', '789123456'],
        'ultima_visita': [datetime.now() - timedelta(days=i*30) for i in range(5)],
        'tipo': ['Frecuente', 'Nuevo', 'Frecuente', 'Corporativo', 'Nuevo']
    }
    clientes = pd.DataFrame(clientes_data)
    
    # Reservas
    reservas_data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'cliente_id': [1, 2, 3, 4, 5, 1, 3, 2, 4, 5],
        'destino': ['París', 'Nueva York', 'Tokio', 'Roma', 'Londres', 'Bali', 'Cancún', 'Madrid', 'Berlín', 'Sídney'],
        'fecha_salida': [datetime.now() + timedelta(days=i*15) for i in range(10)],
        'fecha_regreso': [datetime.now() + timedelta(days=i*15+7) for i in range(10)],
        'estado': ['Confirmada', 'Pendiente', 'Confirmada', 'Cancelada', 'Confirmada', 
                  'Pendiente', 'Confirmada', 'Confirmada', 'Pendiente', 'Confirmada'],
        'monto': [1200, 850, 2100, 950, 1100, 1750, 1250, 900, 1300, 2200]
    }
    reservas = pd.DataFrame(reservas_data)
    
    # Ventas mensuales
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    ventas_data = {
        'mes': meses,
        'ventas': [12500, 13200, 15000, 14200, 16800, 17500, 19200, 18500, 17300, 16200, 15500, 19800],
        'clientes_nuevos': [12, 15, 18, 14, 20, 22, 25, 21, 19, 17, 15, 24]
    }
    ventas = pd.DataFrame(ventas_data)
    
    return clientes, reservas, ventas

# Inicializar datos
clientes, reservas, ventas = cargar_datos()

# Sidebar para navegación
st.sidebar.title("✈️ Agencia de Viajes")
pagina = st.sidebar.radio("Navegación", ["Dashboard", "Reservas", "Facturación", "Itinerarios", "Reportes", "CRM", "Usuarios"])

# Página: Dashboard
if pagina == "Dashboard":
    st.title("Dashboard de Gestión - Agencia de Viajes")
    
    # Métricas clave
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ventas del Mes", f"${ventas['ventas'].iloc[-1]:,}")
    with col2:
        st.metric("Reservas Activas", f"{len(reservas[reservas['estado'] == 'Confirmada'])}")
    with col3:
        st.metric("Clientes Nuevos", f"{ventas['clientes_nuevos'].iloc[-1]}")
    with col4:
        ocupacion = 78
        st.metric("Tasa de Ocupación", f"{ocupacion}%")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.line_chart(ventas.set_index('mes')['ventas'])
    
    with col2:
        destinos_count = reservas['destino'].value_counts()
        st.bar_chart(destinos_count)
    
    # Reservas recientes
    st.subheader("Reservas Recientes")
    st.dataframe(reservas.sort_values('fecha_salida', ascending=False).head(5))

# Página: Reservas
elif pagina == "Reservas":
    st.title("Gestión de Reservas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Sistemas de Reservas Integrados")
        sistemas = st.selectbox("Seleccionar Sistema", ["Amadeus", "Sabre", "Travelport", "Sistema Local"])
        
        if sistemas:
            st.success(f"Conectado a {sistemas}")
            st.dataframe(reservas)
    
    with col2:
        st.subheader("Nueva Reserva")
        with st.form("nueva_reserva"):
            cliente = st.selectbox("Cliente", clientes['nombre'])
            destino = st.text_input("Destino")
            fecha_salida = st.date_input("Fecha de Salida")
            fecha_regreso = st.date_input("Fecha de Regreso")
            monto = st.number_input("Monto", min_value=0)
            
            if st.form_submit_button("Crear Reserva"):
                st.success("Reserva creada exitosamente")

# Página: Facturación
elif pagina == "Facturación":
    st.title("Sistema de Facturación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generar Factura/Boleta")
        with st.form("facturacion_form"):
            tipo_documento = st.radio("Tipo de Documento", ["Boleta", "Factura"])
            cliente = st.selectbox("Cliente", clientes['nombre'])
            reserva = st.selectbox("Reserva", reservas['id'])
            monto = st.number_input("Monto", min_value=0)
            
            if st.form_submit_button("Generar Documento"):
                st.success(f"{tipo_documento} generada exitosamente")
                st.info(f"Documento: {tipo_documento} #{np.random.randint(1000, 9999)}")
    
    with col2:
        st.subheader("Documentos Emitidos")
        docs_data = {
            'fecha': [datetime.now() - timedelta(days=i) for i in range(5)],
            'tipo': ['Factura', 'Boleta', 'Factura', 'Boleta', 'Factura'],
            'cliente': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez'],
            'monto': [1200, 850, 2100, 950, 1100]
        }
        docs = pd.DataFrame(docs_data)
        st.dataframe(docs)

# Página: Itinerarios
elif pagina == "Itinerarios":
    st.title("Generador de Itinerarios")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Crear Itinerario")
        with st.form("itinerario_form"):
            cliente = st.selectbox("Cliente", clientes['nombre'])
            destino = st.text_input("Destino")
            fecha_salida = st.date_input("Fecha de Salida")
            fecha_regreso = st.date_input("Fecha de Regreso")
            
            if st.form_submit_button("Generar Itinerario"):
                st.success("Itinerario generado exitosamente")
    
    with col2:
        st.subheader("Vista Previa Itinerario")
        st.info("""
        **Itinerario de Viaje - París**
        Cliente: Ana García
        Fechas: 15 Nov - 22 Nov 2023
        
        **Detalles:**
        - 15 Nov: Vuelo SALIDA 08:00 → Llegada 12:00
        - 15 Nov: Check-in Hotel Mercure 14:00
        - 16 Nov: Tour Torre Eiffel 10:00
        - 17 Nov: Excursión Versalles 09:00
        - 21 Nov: Día libre
        - 22 Nov: Vuelo REGRESO 18:00 → Llegada 22:00
        """)

# Página: Reportes
elif pagina == "Reportes":
    st.title("Reportes de Ventas")
    
    reporte_tipo = st.selectbox("Tipo de Reporte", [
        "Ventas por Mes", 
        "Destinos Populares", 
        "Clientes por Tipo",
        "Estado de Reservas"
    ])
    
    if reporte_tipo == "Ventas por Mes":
        st.line_chart(ventas.set_index('mes')['ventas'])
    
    elif reporte_tipo == "Destinos Populares":
        destinos_count = reservas['destino'].value_counts()
        st.bar_chart(destinos_count)
    
    elif reporte_tipo == "Clientes por Tipo":
        tipo_count = clientes['tipo'].value_counts()
        st.bar_chart(tipo_count)
    
    elif reporte_tipo == "Estado de Reservas":
        estado_count = reservas['estado'].value_counts()
        st.bar_chart(estado_count)
    
    # Opción para exportar reportes
    st.download_button(
        label="Exportar Reporte a CSV",
        data=ventas.to_csv().encode('utf-8'),
        file_name='reporte_ventas.csv',
        mime='text/csv'
    )

# Página: CRM
elif pagina == "CRM":
    st.title("CRM - Gestión de Clientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Base de Clientes")
        st.dataframe(clientes)
    
    with col2:
        st.subheader("Añadir Nuevo Cliente")
        with st.form("nuevo_cliente"):
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")
            tipo = st.selectbox("Tipo de Cliente", ["Nuevo", "Frecuente", 'Corporativo', 'VIP'])
            
            if st.form_submit_button("Guardar Cliente"):
                st.success("Cliente añadido exitosamente")
    
    st.subheader("Historial de Interacciones")
    interacciones_data = {
        'fecha': [datetime.now() - timedelta(days=i) for i in range(5)],
        'cliente': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez'],
        'tipo': ['Llamada', 'Email', 'Reunión', 'Llamada', 'Email'],
        'resultado': ['Cotización enviada', 'Reserva confirmada', 'Consulta respondida', 'Re-programación', 'Seguimiento']
    }
    interacciones = pd.DataFrame(interacciones_data)
    st.dataframe(interacciones)

# Página: Usuarios
elif pagina == "Usuarios":
    st.title("Gestión de Usuarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Usuarios del Sistema")
        usuarios_data = {
            'usuario': ['admin', 'ana.garcia', 'carlos.lopez', 'maria.rodriguez'],
            'nombre': ['Administrador', 'Ana García', 'Carlos López', 'María Rodríguez'],
            'rol': ['Administrador', 'Agente', 'Supervisor', 'Agente'],
            'ultimo_acceso': [datetime.now() - timedelta(hours=2), 
                             datetime.now() - timedelta(days=1), 
                             datetime.now() - timedelta(hours=5), 
                             datetime.now() - timedelta(days=2)]
        }
        usuarios = pd.DataFrame(usuarios_data)
        st.dataframe(usuarios)
    
    with col2:
        st.subheader("Crear Nuevo Usuario")
        with st.form("nuevo_usuario"):
            username = st.text_input("Nombre de usuario")
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email")
            rol = st.selectbox("Rol", ["Administrador", "Agente", "Supervisor", "Consulta"])
            password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Crear Usuario"):
                st.success("Usuario creado exitosamente")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.info("Sistema de Gestión para Agencia de Viajes v1.0 | © 2023")