import numpy as np

# Cria uma grade no espaço [-1.5, 1.5] x [-1.5, 1.5]
x1 = np.linspace(-1.1, 1.1, 50)
x2 = np.linspace(-1.1, 1.1, 50)
X1, X2 = np.meshgrid(x1, x2)

# Empacota em um tensor para o modelo
grid = np.c_[X1.ravel(), X2.ravel()]

X_data = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y_data = np.array([0, 1, 1, 0])

from sklearn.neural_network import MLPClassifier

model = MLPClassifier((2, 4), activation='relu', max_iter=50000, learning_rate_init=0.01)
model.fit(X_data, y_data)

output = model.predict_proba(grid)[:, 1]

output

Z = output.reshape(X1.shape)

import plotly.io as pio
pio.renderers.default = "notebook_connected"

import plotly.graph_objects as go

fig = go.Figure()

# Superfície da saída do modelo
fig.add_trace(go.Surface(
    x=X1,
    y=X2,
    z=Z,
    colorscale='RdBu',
    opacity=0.7,
    showscale=True,
    name="Model Output"
))

# Dados reais do XOR (opcional)
# Exemplo de pontos XOR

fig.add_trace(go.Scatter3d(
    x=X_data[:, 0],
    y=X_data[:, 1],
    z=y_data,
    mode='markers',
    marker=dict(
        size=6,
        color=y_data,
        colorscale='RdBu',
        line=dict(width=1)
    ),
    name='XOR Data'
))

fig.update_layout(
    title='XOR Model Decision Surface',
    scene=dict(
        xaxis_title='Feature 1',
        yaxis_title='Feature 2',
        zaxis_title='Output / Label'
    )
)
fig.update_layout(
    title='XOR Model Decision Surface',
    scene=dict(
        xaxis=dict(title='Feature 1', range=[-0.2, 1.2]),
        yaxis=dict(title='Feature 2', range=[-0.2, 1.2]),
        zaxis=dict(title='Output / Label'),
    ),
    width=800,
    height=600
)
fig.show()

from plotly.subplots import make_subplots

# ==== Cria subplots com 2 cenas 3D ====
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scene'}, {'type': 'scene'}]],  # Dois gráficos 3D
    subplot_titles=("Superfície do Modelo", "Pontos XOR")
)

# ==== Primeiro gráfico: Superfície ====
fig.add_trace(go.Surface(
    x=X1,
    y=X2,
    z=Z,
    colorscale='RdBu',
    opacity=0.7,
    showscale=False,
    name="Model Output"
), row=1, col=1)
fig.add_trace(go.Scatter3d(
    x=X_data[:, 0],
    y=X_data[:, 1],
    z=y_data,
    mode='markers',
    marker=dict(
        size=6,
        color=y_data,
        colorscale='RdBu',
        line=dict(width=1)
    ),
    name='XOR Data'
), row=1, col=1)

# ==== Segundo gráfico: Pontos do XOR ====
fig.add_trace(go.Scatter3d(
    x=X_data[:, 0],
    y=X_data[:, 1],
    z=y_data,
    mode='markers',
    marker=dict(
        size=8,
        color=y_data,
        colorscale='RdBu',
        line=dict(width=2, color='black')
    ),
    name='XOR Data'
), row=1, col=2)

# ==== Configura os eixos de cada subplot ====
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Feature 1', range=[-0.2, 1.2]),
        yaxis=dict(title='Feature 2', range=[-0.2, 1.2]),
        zaxis=dict(title='Output / Label')
    ),
    scene2=dict(
        xaxis=dict(title='Feature 1', range=[-0.2, 1.2]),
        yaxis=dict(title='Feature 2', range=[-0.2, 1.2]),
        zaxis=dict(title='Output / Label')
    ),
    title="XOR Model Surface and Data Points",
    width=1000,
    height=600
)

fig.show()

