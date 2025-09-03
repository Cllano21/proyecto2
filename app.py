import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import base64
import io

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
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'nombre': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez', 
                  'Pedro Gómez', 'Sofía Hernández', 'Diego Ramírez', 'Elena Castro', 'Miguel Díaz'],
        'email': ['ana@email.com', 'carlos@email.com', 'maria@email.com', 'juan@email.com', 'laura@email.com',
                 'pedro@email.com', 'sofia@email.com', 'diego@email.com', 'elena@email.com', 'miguel@email.com'],
        'telefono': ['123456789', '987654321', '456789123', '321654987', '789123456',
                    '159753486', '357159486', '258369147', '147258369', '369258147'],
        'ultima_visita': [datetime.now() - timedelta(days=i*30) for i in range(10)],
        'tipo': ['Frecuente', 'Nuevo', 'Frecuente', 'Corporativo', 'Nuevo', 
                'Frecuente', 'Corporativo', 'Nuevo', 'Frecuente', 'VIP']
    }
    clientes = pd.DataFrame(clientes_data)
    
    # Reservas
    reservas_data = {
        'id': range(1, 21),
        'cliente_id': [1, 2, 3, 4, 5, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5],
        'destino': ['París', 'Nueva York', 'Tokio', 'Roma', 'Londres', 'Bali', 'Cancún', 'Madrid', 'Berlín', 'Sídney',
                   'Barcelona', 'Dubái', 'Praga', 'Ámsterdam', 'Estambul', 'Lisboa', 'Viena', 'Atenas', 'El Cairo', 'Buenos Aires'],
        'fecha_salida': [datetime.now() + timedelta(days=i*15) for i in range(20)],
        'fecha_regreso': [datetime.now() + timedelta(days=i*15+7) for i in range(20)],
        'estado': ['Confirmada', 'Pendiente', 'Confirmada', 'Cancelada', 'Confirmada', 
                  'Pendiente', 'Confirmada', 'Confirmada', 'Pendiente', 'Confirmada',
                  'Confirmada', 'Pendiente', 'Confirmada', 'Cancelada', 'Confirmada',
                  'Pendiente', 'Confirmada', 'Confirmada', 'Pendiente', 'Confirmada'],
        'monto': [1200, 850, 2100, 950, 1100, 1750, 1250, 900, 1300, 2200,
                 1400, 1950, 1050, 0, 1650, 1850, 1150, 1350, 0, 2050]
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
try:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1940/1940616.png", width=100)
except:
    st.sidebar.write("Logo no disponible")

pagina = st.sidebar.radio("Navegación", ["Dashboard", "Reservas", "Facturación", "Itinerarios", "Reportes", "CRM", "Usuarios"])

# Página: Dashboard
if pagina == "Dashboard":
    st.title("Dashboard de Gestión - Agencia de Viajes")
    
    # Métricas clave
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ventas_mes_actual = ventas['ventas'].iloc[-1]
        st.metric("Ventas del Mes", f"${ventas_mes_actual:,}")
    with col2:
        reservas_activas = len(reservas[reservas['estado'] == 'Confirmada'])
        st.metric("Reservas Activas", f"{reservas_activas}")
    with col3:
        clientes_nuevos = ventas['clientes_nuevos'].iloc[-1]
        st.metric("Clientes Nuevos", f"{clientes_nuevos}")
    with col4:
        ocupacion = 78  # Ejemplo
        st.metric("Tasa de Ocupación", f"{ocupacion}%")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ventas = px.line(ventas, x='mes', y='ventas', title='Ventas Mensuales')
        st.plotly_chart(fig_ventas, use_container_width=True)
    
    with col2:
        destinos_count = reservas['destino'].value_counts().reset_index()
        destinos_count.columns = ['destino', 'reservas']
        fig_destinos = px.bar(destinos_count, x='destino', y='reservas', title='Reservas por Destino')
        st.plotly_chart(fig_destinos, use_container_width=True)
    
    # Reservas recientes
    st.subheader("Reservas Recientes")
    reservas_recientes = reservas.sort_values('fecha_salida', ascending=False).head(5)
    st.dataframe(reservas_recientes[['destino', 'fecha_salida', 'fecha_regreso', 'estado', 'monto']])

# Página: Reservas
elif pagina == "Reservas":
    st.title("Gestión de Reservas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Sistemas de Reservas Integrados")
        sistemas = st.selectbox("Seleccionar Sistema", ["Amadeus", "Sabre", "Travelport", "Sistema Local"])
        
        if sistemas:
            st.success(f"Conectado a {sistemas}")
            
            # Filtros para las reservas
            estado_filtro = st.multiselect(
                "Filtrar por estado",
                options=reservas['estado'].unique(),
                default=reservas['estado'].unique()
            )
            
            destino_filtro = st.multiselect(
                "Filtrar por destino",
                options=reservas['destino'].unique(),
                default=reservas['destino'].unique()
            )
            
            # Aplicar filtros
            reservas_filtradas = reservas[
                (reservas['estado'].isin(estado_filtro)) & 
                (reservas['destino'].isin(destino_filtro))
            ]
            
            st.dataframe(reservas_filtradas)
    
    with col2:
        st.subheader("Nueva Reserva")
        with st.form("nueva_reserva"):
            cliente = st.selectbox("Cliente", clientes['nombre'])
            destino = st.text_input("Destino")
            fecha_salida = st.date_input("Fecha de Salida")
            fecha_regreso = st.date_input("Fecha de Regreso")
            monto = st.number_input("Monto", min_value=0)
            estado = st.selectbox("Estado", ["Confirmada", "Pendiente", "Cancelada"])
            
            if st.form_submit_button("Crear Reserva"):
                # Aquí iría la lógica para guardar la reserva
                st.success("Reserva creada exitosamente")
                st.balloons()

# Página: Facturación
elif pagina == "Facturación":
    st.title("Sistema de Facturación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generar Factura/Boleta")
        with st.form("facturacion_form"):
            tipo_documento = st.radio("Tipo de Documento", ["Boleta", "Factura"])
            cliente = st.selectbox("Cliente", clientes['nombre'])
            reserva_id = st.selectbox("Reserva", reservas['id'])
            reserva_seleccionada = reservas[reservas['id'] == reserva_id]
            
            if not reserva_seleccionada.empty:
                destino = reserva_seleccionada['destino'].values[0]
                monto = reserva_seleccionada['monto'].values[0]
                
                st.write(f"Destino: {destino}")
                st.write(f"Monto de la reserva: ${monto}")
            
            if st.form_submit_button("Generar Documento"):
                numero_documento = f"{'B' if tipo_documento == 'Boleta' else 'F'}-{np.random.randint(1000, 9999)}"
                st.success(f"{tipo_documento} {numero_documento} generada exitosamente")
    
    with col2:
        st.subheader("Documentos Emitidos")
        # Datos de ejemplo para documentos
        docs_data = {
            'fecha': [datetime.now() - timedelta(days=i) for i in range(10)],
            'tipo': ['Factura', 'Boleta', 'Factura', 'Boleta', 'Factura', 'Boleta', 'Factura', 'Boleta', 'Factura', 'Boleta'],
            'cliente': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez',
                       'Pedro Gómez', 'Sofía Hernández', 'Diego Ramírez', 'Elena Castro', 'Miguel Díaz'],
            'monto': [1200, 850, 2100, 950, 1100, 1750, 1250, 900, 1300, 2200],
            'número': [f"F-{1000+i}" if i % 2 == 0 else f"B-{2000+i}" for i in range(10)]
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
            destino = st.text_input("Destino", "París")
            fecha_salida = st.date_input("Fecha de Salida", datetime.now() + timedelta(days=7))
            fecha_regreso = st.date_input("Fecha de Regreso", datetime.now() + timedelta(days=14))
            hotel = st.text_input("Hotel", "Hotel Mercure Paris Centre Tour Eiffel")
            vuelo_salida = st.text_input("Vuelo de Salida", "IB 3456 - 08:00")
            vuelo_regreso = st.text_input("Vuelo de Regreso", "IB 3457 - 18:00")
            
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
        - 18 Nov: Día libre
        - 19 Nov: Museo del Louvre 14:00
        - 20 Nov: Crucero por el Sena 20:00
        - 21 Nov: Día libre
        - 22 Nov: Vuelo REGRESO 18:00 → Llegada 22:00
        
        **Información de Contacto:**
        - Guía local: Jean Dupont (+33 123456789)
        - Emergencias: +34 912345678
        """)
        
        # Opción para descargar itinerario
        st.download_button(
            label="Descargar Itinerario (PDF)",
            data="Contenido de ejemplo del itinerario",
            file_name="itinerario_paris.pdf",
            mime="application/pdf"
        )

# Página: Reportes
elif pagina == "Reportes":
    st.title("Reportes de Ventas")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Opciones de Reporte")
        reporte_tipo = st.selectbox("Tipo de Reporte", [
            "Ventas por Mes", 
            "Destinos Populares", 
            "Clientes por Tipo",
            "Estado de Reservas"
        ])
        
        fecha_inicio = st.date_input("Fecha Inicio", datetime.now() - timedelta(days=30))
        fecha_fin = st.date_input("Fecha Fin", datetime.now())
    
    with col2:
        if reporte_tipo == "Ventas por Mes":
            fig = px.bar(ventas, x='mes', y='ventas', title='Ventas por Mes')
            st.plotly_chart(fig, use_container_width=True)
        
        elif reporte_tipo == "Destinos Populares":
            destinos_count = reservas['destino'].value_counts().reset_index()
            destinos_count.columns = ['destino', 'reservas']
            fig = px.pie(destinos_count, values='reservas', names='destino', title='Destinos Populares')
            st.plotly_chart(fig, use_container_width=True)
        
        elif reporte_tipo == "Clientes por Tipo":
            tipo_count = clientes['tipo'].value_counts().reset_index()
            tipo_count.columns = ['tipo', 'cantidad']
            fig = px.pie(tipo_count, values='cantidad', names='tipo', title='Clientes por Tipo')
            st.plotly_chart(fig, use_container_width=True)
        
        elif reporte_tipo == "Estado de Reservas":
            estado_count = reservas['estado'].value_counts().reset_index()
            estado_count.columns = ['estado', 'cantidad']
            fig = px.bar(estado_count, x='estado', y='cantidad', title='Estado de Reservas')
            st.plotly_chart(fig, use_container_width=True)
    
    # Opción para exportar reportes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="Exportar Reporte a CSV",
            data=ventas.to_csv(index=False).encode('utf-8'),
            file_name='reporte_ventas.csv',
            mime='text/csv'
        )
    with col2:
        st.download_button(
            label="Exportar a Excel",
            data=ventas.to_csv(index=False).encode('utf-8'),
            file_name='reporte_ventas.xlsx',
            mime='application/vnd.ms-excel'
        )
    with col3:
        if st.button("Imprimir Reporte"):
            st.warning("Función de impresión habilitada. Use la función de impresión de su navegador.")

# Página: CRM
elif pagina == "CRM":
    st.title("CRM - Gestión de Clientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Base de Clientes")
        
        # Filtros para clientes
        tipo_filtro = st.multiselect(
            "Filtrar por tipo",
            options=clientes['tipo'].unique(),
            default=clientes['tipo'].unique()
        )
        
        clientes_filtrados = clientes[clientes['tipo'].isin(tipo_filtro)]
        st.dataframe(clientes_filtrados)
    
    with col2:
        st.subheader("Añadir Nuevo Cliente")
        with st.form("nuevo_cliente"):
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")
            tipo = st.selectbox("Tipo de Cliente", ["Nuevo", "Frecuente", "Corporativo", "VIP"])
            
            if st.form_submit_button("Guardar Cliente"):
                # Aquí iría la lógica para guardar el cliente
                st.success("Cliente añadido exitosamente")
    
    st.subheader("Historial de Interacciones")
    interacciones_data = {
        'fecha': [datetime.now() - timedelta(days=i) for i in range(10)],
        'cliente': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez', 'Laura Sánchez',
                   'Pedro Gómez', 'Sofía Hernández', 'Diego Ramírez', 'Elena Castro', 'Miguel Díaz'],
        'tipo': ['Llamada', 'Email', 'Reunión', 'Llamada', 'Email', 'Llamada', 'Email', 'Reunión', 'Llamada', 'Email'],
        'resultado': ['Cotización enviada', 'Reserva confirmada', 'Consulta respondida', 'Re-programación', 'Seguimiento',
                     'Reserva cancelada', 'Nueva cotización', 'Consulta respondida', 'Reunión agendada', 'Seguimiento']
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
            'usuario': ['admin', 'ana.garcia', 'carlos.lopez', 'maria.rodriguez', 'juan.martinez'],
            'nombre': ['Administrador', 'Ana García', 'Carlos López', 'María Rodríguez', 'Juan Martínez'],
            'rol': ['Administrador', 'Agente', 'Supervisor', 'Agente', 'Agente'],
            'ultimo_acceso': [datetime.now() - timedelta(hours=2), 
                             datetime.now() - timedelta(days=1), 
                             datetime.now() - timedelta(hours=5), 
                             datetime.now() - timedelta(days=2),
                             datetime.now() - timedelta(days=3)]
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
            confirm_password = st.text_input("Confirmar Contraseña", type="password")
            
            if st.form_submit_button("Crear Usuario"):
                if password == confirm_password:
                    st.success("Usuario creado exitosamente")
                else:
                    st.error("Las contraseñas no coinciden")
    
    st.subheader("Permisos de Usuario")
    roles_data = {
        'Rol': ['Administrador', 'Supervisor', 'Agente', 'Consulta'],
        'Reservas': ['Completo', 'Completo', 'Completo', 'Solo lectura'],
        'Facturación': ['Completo', 'Completo', 'Crear', 'Solo lectura'],
        'Reportes': ['Completo', 'Completo', 'Solo lectura', 'Solo lectura'],
        'CRM': ['Completo', 'Completo', 'Completo', 'Solo lectura'],
        'Usuarios': ['Completo', 'Solo lectura', 'Ninguno', 'Ninguno']
    }
    roles_df = pd.DataFrame(roles_data)
    st.dataframe(roles_df)

# Pie de página
st.sidebar.markdown("---")
st.sidebar.info("Sistema de Gestión para Agencia de Viajes v1.0")
st.sidebar.info(f"© {datetime.now().year} - Todos los derechos reservados")

# Nota: Para una implementación real, necesitarías:
# 1. Conexión a base de datos real
# 2. Autenticación de usuarios
# 3. Lógica de negocio completa
# 4. Validación de datos