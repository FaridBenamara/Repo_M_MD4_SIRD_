import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from euler_sird import euler_sird

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Paramètres optimaux
best_beta = 0.3789473684210526
best_gamma = 0.11157894736842105
best_micro = 0.010

app.layout = html.Div([
    html.H1('SIRD - Impact des Mesures de Contrôle', style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Contrôles
    html.Div([
        html.Label('Réduction du taux de transmission (β) :'),
        dcc.Slider(
            id='beta-reduction',
            min=0,
            max=1,
            step=0.1,
            value=0.5,
            marks={i/10: f'{i*10}%' for i in range(11)}
        )
    ], style={'width': '80%', 'margin': '0 auto', 'padding': '20px'}),
    
    # Graphiques
    html.Div([
        dcc.Graph(id='sird-graph', style={'height': '600px'}),
        html.Div([
            html.Div(id='r0-stats', style={'textAlign': 'center', 'padding': '20px'})
        ])
    ])
])

@app.callback(
    [Output('sird-graph', 'figure'),
     Output('r0-stats', 'children')],
    [Input('beta-reduction', 'value')]
)
def update_graph(reduction):
    # Calcul des paramètres avec et sans intervention
    new_beta = best_beta * (1 - reduction)
    
    # Simulations
    time_avant, sus_avant, inf_avant, heal_avant, dead_avant = euler_sird(
        [best_beta, best_gamma, best_micro],
        [0.99, 0.01, 0, 0],
        0.01,
        90
    )
    
    time_apres, sus_apres, inf_apres, heal_apres, dead_apres = euler_sird(
        [new_beta, best_gamma, best_micro],
        [0.99, 0.01, 0, 0],
        0.01,
        90
    )
    
    # Création de la figure
    fig = go.Figure()
    
    # Ajout des courbes pour chaque compartiment
    categories = {
        'Susceptibles': (sus_avant, sus_apres, 'rgba(255,0,0,0.8)'),
        'Infectés': (inf_avant, inf_apres, 'rgba(0,0,255,0.8)'),
        'Rétablis': (heal_avant, heal_apres, 'rgba(0,255,0,0.8)'),
        'Décédés': (dead_avant, dead_apres, 'rgba(0,0,0,0.8)')
    }
    
    for name, (avant, apres, color) in categories.items():
        fig.add_trace(go.Scatter(
            x=time_avant, y=avant,
            name=f'{name} (sans intervention)',
            line=dict(color=color)
        ))
        fig.add_trace(go.Scatter(
            x=time_apres, y=apres,
            name=f'{name} (avec intervention)',
            line=dict(color=color, dash='dash')
        ))
    
    fig.update_layout(
        title='Évolution des compartiments SIRD',
        xaxis_title='Jours',
        yaxis_title='Proportion de la population',
        hovermode='x unified',
        legend={'orientation': 'h', 'y': -0.2}
    )
    
    # Calcul des statistiques
    R0_avant = best_beta / (best_gamma + best_micro)
    R0_apres = new_beta / (best_gamma + best_micro)
    
    stats = html.Div([
        html.H3(f'R0 sans intervention: {R0_avant:.2f}'),
        html.H3(f'R0 avec intervention: {R0_apres:.2f}'),
        html.H3(f'Réduction du R0: {((R0_avant - R0_apres)/R0_avant)*100:.1f}%')
    ])
    
    return fig, stats

if __name__ == '__main__':
    app.run_server(debug=True) 