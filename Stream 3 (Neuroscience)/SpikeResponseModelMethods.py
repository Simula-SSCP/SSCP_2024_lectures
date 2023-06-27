from matplotlib import pyplot as plt

def plotResults(time, potential, spike_times, current, parameters):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    ax1.plot(time, potential)
    ax1.set_ylabel(r"$v(t)$ [mV]")
    ax1.axhline(parameters["v_thresh"], ls='--', lw=.5, label='Threshold')
    ax2.eventplot(spike_times)
    ax2.set_ylabel(r"$S(t)$")
    ax2.set_yticks([])
    ax3.plot(time, current(time))
    ax3.set_xlabel(r"Time [ms]")
    ax3.set_ylabel(r"$I_{ext}(t)$ [nA]")
    plt.show()