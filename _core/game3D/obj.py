def load(filename, texturs=False):
    vertices = []
    faces = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':
                x = float(parts[1]); y = float(parts[2]); z = float(parts[3])
                vertices.append((x, y, z))
            elif parts[0] == 'f':
                indices = []
                for part in parts[1:]:
                    idx = int(part.split('/')[0]) - 1
                    indices.append(idx)
                if len(indices) == 3:
                    faces.append(indices)
                elif len(indices) > 3:
                    for i in range(1, len(indices) - 1):
                        faces.append([indices[0], indices[i], indices[i+1]])

    return vertices, faces
