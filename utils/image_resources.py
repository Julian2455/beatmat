from utils import resource_path

IMAGE_MAP = {
    "agregar-usuario2": resource_path("resources/images/agregar-usuario2.png"),
    "anterior_1": resource_path("resources/images/anterior (1).png"),
    "anterior": resource_path("resources/images/anterior.png"),
    "avatar": resource_path("resources/images/avatar.png"),
    "basura": resource_path("resources/images/basura.png"),
    "boligrafo": resource_path("resources/images/boligrafo.png"),
    "borrar": resource_path("resources/images/borrar.png"),
    "buscar": resource_path("resources/images/buscar.png"),
    "busqueda": resource_path("resources/images/busqueda.png"),
    "caja_registradora": resource_path("resources/images/caja-registradora.png"),
    "estadisticas": resource_path("resources/images/estadisticas.png"),
    "extintor_de_incendios": resource_path("resources/images/extintor-de-incendios.png"),
    "extintor": resource_path("resources/images/extintor.png"),
    "fecha_de_vencimiento": resource_path("resources/images/fecha-de-vencimiento.png"),
    "flecha_anterior": resource_path("resources/images/flecha-anterior.png"),
    "flecha_siguiente": resource_path("resources/images/flecha-siguiente.png"),
    "google_mas": resource_path("resources/images/google-mas.png"),
    "lupa": resource_path("resources/images/lupa.png"),
    "mas": resource_path("resources/images/mas.png"),
    "nueva_cuenta": resource_path("resources/images/nueva-cuenta.png"),
    "personas": resource_path("resources/images/personas.png"),
    "proximo_1": resource_path("resources/images/proximo (1).png"),
    "salario": resource_path("resources/images/salario.png"),
    "sssiguiente": resource_path("resources/images/sssiguiente.png"),
    "flecha_izquierda": resource_path("resources/images/flecha-izquierda.png"),
    "imprimir":resource_path("resources/images/imprimir.png"),
    "print":resource_path("resources/images/print.png"),
    "encabezado-impresion":resource_path("resources/images/encabezado-impresion.png"),
    "encabezado-impresion-dos":resource_path("resources/images/encabezado-impresion-dos.png"),
    "notificacion": resource_path("resources/images/notificacion"),
    "extintor-de-incendios(1)": resource_path("resources/images/extintor-de-incendios(1)")

}

def get_image(name):
    return IMAGE_MAP.get(name, "")
