from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import decimal

# Modelo para Categorías de Productos
class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        db_index=True, # Índice para búsquedas rápidas
        verbose_name=_("Nombre de Categoría")
    )

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")
        ordering = ['nombre'] # Ordenar alfabéticamente por defecto

    def __str__(self):
        return self.nombre

# Modelo para Tipos de Motocicleta
class TipoMoto(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Tipo de Moto"),
        help_text=_("Ej: Trabajo, Cuatrimoto, Semiautomática, Deportiva")
    )

    class Meta:
        verbose_name = _("Tipo de Moto")
        verbose_name_plural = _("Tipos de Moto")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# --- Modelo Proveedor (sin campo 'notas') ---
class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name=_("Nombre del Proveedor")
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Teléfono")
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_("Correo Electrónico")
    )
    direccion = models.TextField(
        blank=True,
        verbose_name=_("Dirección")
    )
    # --- Campo notas ELIMINADO ---
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de Creación")
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última Actualización")
    )

    class Meta:
        verbose_name = _("Proveedor")
        verbose_name_plural = _("Proveedores")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Modelo Principal de Producto (sin cambios en esta revisión)
class Producto(models.Model):
    nombre = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_("Nombre del Producto")
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name=_("Descripción"),
        help_text=_("Detalles adicionales del producto (opcional).")
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name=_("Categoría")
    )
    tipo_moto = models.ForeignKey(
        TipoMoto,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='productos',
        verbose_name=_("Aplica a Tipo de Moto"),
        help_text=_("Opcional: Selecciona si este producto es específico para un tipo de moto.")
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_("SKU (Código Interno)"),
        help_text=_("Código único interno para identificar el producto en el taller.")
    )
    codigo_barras = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_("Código de Barras (Fabricante)"),
        help_text=_("Código de barras EAN/UPC del producto, si lo tiene.")
    )
    marca = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        verbose_name=_("Marca")
    )
    stock_actual = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Stock Actual"),
        help_text=_("Cantidad de unidades disponibles en inventario.")
    )
    stock_minimo = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Stock Mínimo"),
        help_text=_("Cantidad mínima antes de necesitar reordenar.")
    )
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=decimal.Decimal('0.00'),
        verbose_name=_("Precio de Compra"),
        help_text=_("Costo al que se adquirió el producto.")
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=decimal.Decimal('0.00'),
        verbose_name=_("Precio de Venta"),
        help_text=_("Precio al que se vende el producto al público.")
    )
    proveedor = models.ForeignKey(
        Proveedor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='productos',
        verbose_name=_("Proveedor"),
        help_text=_("Proveedor al que se le compra este producto.")
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de Creación")
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última Actualización")
    )

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.marca})" if self.marca else self.nombre

    def clean(self):
        if self.precio_compra < 0:
            raise ValidationError({'precio_compra': _("El precio de compra no puede ser negativo.")})
        if self.precio_venta < 0:
            raise ValidationError({'precio_venta': _("El precio de venta no puede ser negativo.")})

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo

