import Color

def circle(y, r):
    ps = []
    N = 100
    for t in range(N):
        t = t * 2 * np.pi / N
        x = np.cos(t) * r
        z = np.sin(t) * r
        ps.append((x, y, z))
    return ps
    
def sphere(r):
    ps = []
    N = 10
    for t in range(N):
        t = t * np.pi / N
        rr = np.sin(t) * r
        y = np.cos(t) * r
        ps = ps + circle(y, rr)
    return ps
        
def cone(ctl):
    ps = []
    N = 10
    for t in range(N):
        ps = ps + circle(t * 2, t + 4)
    return ps

def line_z(l, x, y):
    ps = []
    for z in range(l):
        ps.append((x, y, z))
    return ps

def plane_xz(a, b):
    ps = []
    for x in range(a):
        ps = ps + line_z(b, x, -1)
    return ps

def build_spectrum(a, b, mlc):
    ps = plane_xz(a, b)
    def block_func(x, y, z):
        return Color.find_best_block(Color.coords_to_rgb(x / a, z / b))
    mlc.set_blocks_with_select_func(ps, block_func)