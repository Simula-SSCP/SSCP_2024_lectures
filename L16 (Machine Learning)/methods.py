import numpy as np

def poisson_neurons(ncells, rate, duration=6000.0):
    """
    Parameters:
        ncells, int: number of neurons
        rate, float: firing rate in Hz
        duration, float: duration of simulation in ms
    Returns:
        list of arrays: spike times for each neuron
    """
    def generate_spike_train():
        # returns: array of spike times in ms
        t = 0
        spikes = []

        while t < duration:
            dt = np.random.exponential(1.0 / (rate / 1000.0))
            t += dt
            if t < duration:
                spikes.append(t)

        return np.array(spikes)
    return [generate_spike_train() for i in range(ncells)]

def spike_trains_to_binary(spike_timess, duration=6000.0, bin_size=1.0):
    """
    Parameters:
        spike_timess, list of arrays: spike times in ms
        duration, float: duration of simulation in ms
        bin_size, float: size of bins in ms
    Returns:
        (ncells,T) 2D-array: binary spike trains
    """
    def spike_train_to_binary(spike_times):
        n_bins = int(duration / bin_size)
        binary = np.zeros(n_bins)
        for spike_time in spike_times:
            bin_idx = int(spike_time / bin_size)
            if bin_idx < n_bins:
                binary[bin_idx] = 1
        return binary
    return np.array([spike_train_to_binary(spike_times) for spike_times in spike_timess])

def lif_integrate(spike_trains_exc, spike_trains_inh, tau=20.0, dt=1.0, ur=-77.0, u_thresh=-55.0, w_exc=2.0, w_inh=-2.0):
        """
        Parameters:
            spike_trains_exc, (ncells,T): 2D-array of binary spike trains for excitatory neurons
            spike_trains_inh, (ncells,T): 2D-array of binary spike trains for inhibitory neurons
            tau, float: membrane time constant in ms
            dt, float: time step in ms
            ur, float: resting potential in mV
            u_thresh, float: threshold potential in mV
            w_exc, float: excitatory synaptic weight
            w_inh, float: inhibitory synaptic weight
        Returns:
            us, (T,): membrane potentials
            out_spike_train, (T,): output spike train
        """
        # convert to cummulative spike counts
        exc_spike_counts = spike_trains_exc.sum(axis=0)
        inh_spike_counts = spike_trains_inh.sum(axis=0)
        
        us = np.zeros(exc_spike_counts.shape)
        out_spike_train = np.zeros(exc_spike_counts.shape)
        us[0] = ur 
        for i_t in range(len(us) - 1):
            #us[i_t + 1] = us[i_t] - dt*us[i_t] / tau + w_inh*inh_spike_counts[i_t] + w_exc*exc_spike_counts[i_t]
            
            leak = us[i_t] - ur # leak is the difference between current membrane potential and resting potential
            current = w_inh*inh_spike_counts[i_t] + w_exc*exc_spike_counts[i_t] # current is the sum of excitatory and inhibitory currents
            us[i_t + 1] = us[i_t] - dt*leak/tau + current # update membrane potential
            if us[i_t + 1] > u_thresh:
                out_spike_train[i_t+1] = 1.0
                us[i_t + 1] = ur
        return us, out_spike_train

def lif_direct(spike_trains_exc, spike_trains_inh, tau=20, ur=-77.0, u_thresh=-55.0, w_exc=2.0, w_inh=-2.0):
    # convert to cumulative spike counts
    exc_spike_counts = spike_trains_exc.sum(axis=0)
    inh_spike_counts = spike_trains_inh.sum(axis=0)

    def K(spike_counts, weight):
        # kernel function
        t_spike = np.arange(len(spike_counts))
        return np.sum(weight * spike_counts * np.exp(-t_spike[::-1] / tau))
    
    out_spike_train = np.zeros(len(exc_spike_counts))
    us = np.zeros(len(inh_spike_counts))
    t_prev_spike = 0
    for t in range(len(exc_spike_counts)):
        exc_activity = K(exc_spike_counts[t_prev_spike:t+1], w_exc)
        inh_activity = K(inh_spike_counts[t_prev_spike:t+1], w_inh)
        total_activity = ur + exc_activity + inh_activity
        us[t] = total_activity
        if total_activity > u_thresh:
            out_spike_train[t] = 1.0
            t_prev_spike = t
    return us, out_spike_train

def lif_with_adaptation(spike_trains_exc, spike_trains_inh, dt, T, u_rest=-70, u_thresh=-50, tau_m=20, tau_w=200, a=0.5, b=7, R=1, w_exc=2.0, w_inh=-2.0):
    """
    Parameters:
        spike_trains_exc: (ncells,T) array-like
            Binary spike trains for excitatory neurons
        spike_trains_inh: (ncells,T) array-like
            Binary spike trains for inhibitory neurons
        dt: float
            Time step in ms
        T: int
            Total simulation time in ms
        u_rest: float
            Resting membrane potential in mV
        u_thresh: float, optional
            Threshold membrane potential for spike generation in mV
        tau_m: float
            Membrane time constant in ms
        tau_w: float, optional
            Adaptation time constant in ms
        a: float
            Subthreshold adaptation conductance
        b: float, optional
            Spike-triggered adaptation in pA
        R: float
            Membrane resistance in MΩ
        w_exc: float
            Excitatory synaptic weight
        w_inh: float
            Inhibitory synaptic weight
    Returns:
        u: (T,) array-like
            Membrane potential
        spikes: (T,) array-like
            Spike train (0 for no spike, 1 for spike)
    """
    I = w_exc*spike_trains_exc.sum(axis=0) + w_inh*spike_trains_inh.sum(axis=0)
    num_iters = int(T/dt)
    u = np.zeros(num_iters)
    w = np.zeros(num_iters)
    spikes = np.zeros(num_iters)
    u[0] = u_rest
    for i in range(1, num_iters):
        du_dt = (-(u[i-1] - u_rest) + R * I[i-1] - R * a * w[i-1]) / tau_m
        dw_dt = (a * (u[i-1] - u_rest) - w[i-1]) / tau_w
        u[i] = u[i-1] + dt * du_dt
        w[i] = w[i-1] + dt * dw_dt
        if u[i] >= u_thresh:
            u[i] = u_rest
            w[i] = w[i] + b
            spikes[i] = 1
    return u, spikes
