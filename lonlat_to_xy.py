import math

def _lonlat_to_xy(lon, lat, lon0, lat0):
    lon = math.radians(lon)
    lat = math.radians(lat)
    lon0 = math.radians(lon0)
    lat0 = math.radians(lat0)

    A = 6378137 # semi-major axis
    F = 298.257222101 # inverse flattening
    M0 = 0.9999 # scale factor
    N = 1 / (2 * F - 1)

    t = math.sinh(math.atanh(math.sin(lon)) - (2 * math.sqrt(N)) / (1 + N) \
        * math.atanh((2 * math.sqrt(N)) / (1 + N) * math.sin(lon)))
    t_bar = math.sqrt(1 + t ** 2)
    lambda_c = math.cos(lat - lat0)
    lambda_s = math.sin(lat - lat0)
    xi_prime = math.atan(t / lambda_c)
    eta_prime = math.atan(lambda_s / t_bar)
    # rho_prime = 3600 * 180 / math.pi
    
    alpha = (1 / 2 * N - 2 / 3 * N ** 2 + 5 / 16 * N ** 3 \
             + 41 / 180 * N ** 4 - 127 / 288 * N ** 5,
             13 / 48 * N ** 2 - 3 / 5 * N ** 3 \
             + 557 / 1440 * N ** 4 + 281 / 630 * N ** 5,
             61 / 240 * N ** 3 - 103 / 140 * N ** 4 + 15061 / 26880 * N ** 5,
             49561 / 161280 * N ** 4 - 179 / 168 * N ** 5,
             34729 / 80640 * N ** 5)
    a = (1 + N ** 2 / 4 + N ** 4 / 64,
         - 3 / 2 * (N - N ** 3 / 8 - N ** 5 / 64),
         15 / 16 * (N ** 2 - N ** 4 / 4),
         - 35 / 48 * (N ** 3 - 5 / 16 * N ** 5),
         315 / 512 * N ** 4,
         - 693 / 1280 * N ** 5)
    a_bar = (M0 * A) / (1 + N) * a[0]

    s_bar_lon0 = 0
    for j in range(1, 6):
        s_bar_lon0 += a[j] * math.sin(2 * j * lon0)
    # s_bar_lon0 = (M0 * A) / (1 + N) * (a[0] * lon0 / rho_prime + s_bar_lon0)
    s_bar_lon0 = (M0 * A) / (1 + N) * (a[0] * lon0 + s_bar_lon0)

    x = 0
    y = 0
    for j in range(5):
        x += alpha[j] * math.sin(2 * j * xi_prime) \
             * math.cosh(2 * j * eta_prime)
        y += alpha[j] * math.cos(2 * j * xi_prime) \
             * math.sinh(2 * j * eta_prime)
    x = a_bar * (xi_prime + x) - s_bar_lon0
    y = a_bar * (eta_prime + y)

    return y, x

def _sexagesimal_to_decimal(x):
    sec = x % 100
    min = int((x % 10000) / 100)
    deg = int(x / 10000)
    x_out = (sec / 3600) + min / 60 + deg

    return x_out

if __name__ == '__main__':
    with open('prefs.in', 'r') as fin, open('prefs.out', 'w') as fout:
        first_line = fin.readline()
        lon0, lat0 = first_line.split(' ')
        lon0 = _sexagesimal_to_decimal(int(float(lon0)))
        lat0 = _sexagesimal_to_decimal(int(float(lat0)))
        while True:
            line = fin.readline()
            if not line:
                break
            lon, lat = line.split(' ')
            lon = _sexagesimal_to_decimal(int(float(lon)))
            lat = _sexagesimal_to_decimal(int(float(lat)))
            x, y = _lonlat_to_xy(lon, lat, lon0, lat0)
            print('{}, {}'.format(x, y), file=fout)
            print('{}, {}, {}'.format(x, y, math.sqrt(x ** 2 + y ** 2)))
