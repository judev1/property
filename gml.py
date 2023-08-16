from matplotlib import pyplot as plt
from shapely.geometry import Point


def view(gdf, display=lambda i: str(i)):

    ax = gdf.boundary.plot()
    fig = ax.get_figure()

    info = ax.annotate(
        '', xy=(0,0), xytext=(20,20),
        textcoords='offset points',
        bbox=dict(boxstyle='round', fc='w'),
        arrowprops=dict(arrowstyle='->')
    )
    info.set_visible(False)

    def hover(event):
        visible = info.get_visible()
        if event.inaxes == ax:
            point = Point(event.xdata, event.ydata)
            polygons = gdf['geometry'].contains(point)
            for i, polygon in enumerate(polygons):
                if polygon:
                    if visible and info.get_text() == str(i):
                        return
                    info.xy = gdf['geometry'][i].centroid.coords[0]
                    info.set_text(display(i))
                    info.set_visible(True)
                    fig.canvas.draw_idle()
                    return
        if visible:
            info.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hover)
    plt.show()