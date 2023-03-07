import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create cube vertices
vertices = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1,- 1 , 1)]

# Create cube faces
faces = [(0, 1 , 2 , 3 ), (4 , 5 , 6 , 7 ), (0 , 4 , 5 , 1 ), (2 , 6 , 7 , 3 ), (0 , 3 , 7 , 4 ), (2 , 5 , 6 , 1 )]

# Plot cube faces and edges
for face in faces:

    x = [vertices[i][0] for i in face]

    y = [vertices[i][1] for i in face]

    z = [vertices[i][2] for i in face]
    print(face, x, y, z)
    ax.plot_trisurf(x=x, y=y, z=z)

     # Display the plot

    plt.show()