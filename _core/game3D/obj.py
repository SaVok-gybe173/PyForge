def load(filename, texturs = False):
    vertices = []
    faces = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                vertices.append((x, y, z))
            elif parts[0] == 'f':
                face_vertices = []
                cld = 0
                for part in parts[1:4]:
                    indices = part.split('/')
                    vertex_index = int(indices[0]) - 1
                    face_vertices.append(vertex_index)
                    cld += 1
                if not texturs:
                    del face_vertices[-1]
                faces.append(face_vertices)
    
    return vertices, faces

