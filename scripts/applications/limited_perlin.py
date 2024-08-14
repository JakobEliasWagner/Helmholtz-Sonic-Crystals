import dash
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from scipy.interpolate import splev, splprep
from skimage import measure

from hsc.noise import LimitedPerlin

# Initialize the Dash app
app = dash.Dash(__name__)

N = 51

app.layout = html.Div(
    [
        dcc.RangeSlider(2, 32, 1, value=[3, 4], id="N"),
        dcc.Slider(
            0,
            32,
            1,
            id="Smoothing",
            value=1,
            tooltip={"placement": "bottom", "always_visible": False},
        ),
        html.Button("Recalculate", id="Recalculate"),
        html.Div(
            [
                html.Div(
                    id="image-container-1",
                    children=[
                        html.Div(
                            [
                                dcc.Graph(id="im1"),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),  # Graph container for image-1
                        html.Div(
                            [
                                dcc.Graph(id="im2"),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),  # Graph container for image-2
                    ],
                    style={"width": "100%", "display": "flex"},
                ),
                html.Div(
                    id="image-container-2",
                    children=[
                        html.Div(
                            [
                                dcc.Graph(id="im3"),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),  # Graph container for image-1
                        html.Div(
                            [
                                dcc.Graph(id="im4"),
                            ],
                            style={"display": "inline-block", "width": "40%"},
                        ),  # Graph container for image-2
                    ],
                    style={"width": "100%", "display": "flex"},
                ),
            ]
        ),
    ]
)


@app.callback(
    [
        Output("im1", "figure"),
        Output("im2", "figure"),
        Output("im3", "figure"),
        Output("im4", "figure"),
    ],
    [
        Input("N", "value"),
        Input("Smoothing", "value"),
        Input("Recalculate", "n_clicks"),
    ],
)
def update_images(n, s, _):
    # Update this function based on the sliders to apply transformations
    noise = LimitedPerlin(n=list(range(n[0], n[1] + 1)), smoothing_steps=s)
    x = np.linspace(-1, 1, N)
    y = np.linspace(-1, 1, N)
    xx, yy = np.meshgrid(x, y)
    points = np.stack([xx.flatten(), yy.flatten()], axis=1)

    images = [noise(points).reshape(N, N) for _ in range(4)]

    figs = []
    for imag in images:
        v_max = np.max(np.abs(imag))
        figs.append(
            px.imshow(
                imag.T,
                zmin=-v_max,
                zmax=v_max,
                color_continuous_scale="RdBu",
                x=x,
                y=y,
                origin="upper",
            )
        )
        contours = measure.find_contours(imag, 0.0, fully_connected="low")
        contour_coords = []
        for contour in contours:
            upper = np.ceil(contour).astype(int)
            lower = np.floor(contour).astype(int)

            dist_x = contour[:, 0] - lower[:, 0]
            exact_x = x[lower[:, 0]] * (1 - dist_x) + x[upper[:, 0]] * dist_x

            dist_y = contour[:, 1] - lower[:, 1]
            exact_y = y[lower[:, 1]] * (1 - dist_y) + y[upper[:, 1]] * dist_y

            contour_coords.append(np.stack([exact_x, exact_y], axis=1))

        for contour in contour_coords:
            if contour.shape[0] <= 10:
                continue
            tck, u = splprep([contour[:, 0], contour[:, 1]], s=0.01, per=True)
            u_new = np.linspace(0, 1, contour.shape[0])
            smooth_contour = splev(u_new, tck)
            figs[-1].add_trace(
                go.Scatter(
                    x=smooth_contour[0],
                    y=smooth_contour[1],
                    mode="lines",
                )
            )

    return figs


if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1")
