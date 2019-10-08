from matplotlib.pyplot import *
from functions.utils_fct import *
from math import ceil
from mpl_toolkits.axes_grid1 import make_axes_locatable
from model.model import Model
from scipy.interpolate import griddata

def print_1D(models, latitude, longitude, models_name, fonctions, fonctions_label, fig_nb, zmin=None, zmax=None,
             delta_z=1, suptitle=None):
    fig = figure(fig_nb)

    nb_plots = ceil(len(fonctions) ** 0.5)

    if zmax is None:
        zmax = np.max([np.max(model.getDepths()) for model in models])

    if zmin is None:
        zmin = 0

    # reduce models to 1d
    depths = np.arange(zmin, zmax + delta_z, delta_z)
    latitudes = [latitude] * len(depths)
    longitudes = [longitude] * len(depths)

    xi = np.array([[latitude, longitude, z] for z in depths])

    models_ = []

    for model in models:
        p1, p2, p3, p4, p5, p6 = model.getParameters(xi).T

        models_.append(Model(latitudes, longitudes, depths, p1, p2, p3, p4, p5, p6))

    # print
    for i in range(len(fonctions)):

        subploti = subplot(nb_plots, nb_plots, i + 1)

        for model_, label in zip(models_, models_name):
            values_ = fonctions[i](model_)

            plot(values_, depths, label=label)

        subploti.xaxis.tick_top()
        subploti.xaxis.set_label_position('top')

        grid(True)
        xlabel(fonctions_label[i])
        ylabel("z [km]")

        ylim(zmax, zmin)

        if i == 0:
            subploti.legend(bbox_to_anchor=(-0.08, 0.3),
                            fancybox=True, shadow=True, ncol=1)

    if suptitle is not None:
        fig.suptitle(suptitle)


def print_models_2D(models, latitude_1, longitude_1, latitude_2, longitude_2, models_name, fonctions, fonctions_label,
                    fig_nb, nb_x, zmin=None, zmax=None, delta_z=1, vmins=None, vmaxs=None, suptitle=None,
                    aspect="auto"):
    fig = figure(fig_nb)

    if zmax is None:
        zmax = np.max([np.max(model.getDepths()) for model in models])

    if zmin is None:
        zmin = 0

    xmin = 0
    xmax = get_distance_km(latitude_1, longitude_1, latitude_1, longitude_2)

    # reduce models to 2d

    depths_ = np.arange(zmin, zmax + delta_z, delta_z)
    depths = np.tile(depths_, nb_x)

    N = []

    for n in range(nb_x):
        N.extend([n] * len(depths_))

    lats_longs = griddata(np.array([0, nb_x]).T, np.array([[latitude_1, latitude_2], [longitude_1, longitude_2]]).T, N)

    latitudes = lats_longs.T[0]
    longitudes = lats_longs.T[1]

    xi = np.array([latitudes, longitudes, depths]).T

    models_ = []

    for model in models:
        p1, p2, p3, p4, p5, p6 = model.getParameters(xi).T

        models_.append(Model(latitudes, longitudes, depths, p1, p2, p3, p4, p5, p6))

    # create vmins/vmaws if is needed

    if vmins is None or vmaxs is None:
        vmins = []

        for fonction in fonctions:
            vmins.append(np.min([np.min(fonction(model)) for model in models]))

        vmaxs = []

        for fonction in fonctions:
            vmaxs.append(np.max([np.max(fonction(model)) for model in models]))

        # for anisotropy center on 1
        if Model.getXi in fonctions:
            index_xi = fonctions.index(Model.getXi)

            xi_min = max([abs(1 - vmins[index_xi]), abs(1 - vmaxs[index_xi])])

            vmins[index_xi] = 1 - xi_min
            vmaxs[index_xi] = 1 + xi_min

    # print
    for i in range(1, len(models_) * len(fonctions) + 1):
        subplot_i = subplot(len(fonctions), len(models_), i)

        model = models_[(i - 1) % len(models_)]
        label = models_name[(i - 1) % len(models_)]

        index_fct = (i - 1) // len(models_)

        data_ = fonctions[index_fct](model)

        cmap = cm.get_cmap('seismic_r', 31)
        cmap.set_bad(color="lime")

        # aspect auto / equal / float

        im = imshow(data_.reshape(nb_x, len(depths_)).T, aspect=aspect, extent=(xmin, xmax, zmax, zmin),
                    cmap=cmap,
                    vmin=vmins[index_fct], vmax=vmaxs[index_fct])

        title(fonctions_label[index_fct] + " | " + label)  # y=1.3
        xlabel("Distance [km]")
        ylabel("z [km]")
        grid(True)
        divider = make_axes_locatable(subplot_i)
        cax = divider.append_axes("right", size="3%", pad=0.05)
        colorbar(im, cax)

    subplots_adjust(hspace=0.8)
    if suptitle is not None:
        fig.suptitle(suptitle)
