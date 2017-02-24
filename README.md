# sanic-example
Example using sanic, pony orm and more.

Para crear un dominio al estilo www.app.dev y así ingresar a la app se debe
cambiar el archivo /etc/hosts en el cual se debe agregar una linea asi
'127.0.0.1 www.app.dev' luego, se debe redirigir el trafico del puerto 8000 (en
este caso) al puerto 80 (puerto por defecto) de esta forma:

```
sudo iptables -t nat -A OUTPUT -o lo -p tcp \
    --dport 80 -j REDIRECT --to-port 6969
```
