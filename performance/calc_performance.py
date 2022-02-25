'''

Calculates the results from latency and throughput measurements, and generates plots for them.
You might need to edit the code to generate plots for different types of messages; see relevant comments for more details

This script should be run with different system arguments for latency and throughput calulcations:

    python calc_performance.py <time_of_measurement> latency <num_of_messages_for_run_1> <num_of_messages_for_run_2> <num_of_messages_for_run_3> ...
    
    python calc_performance.py <time_of_measurement_with_surb> <time_of_measurement_without_surb> throughput <num_of_messages_for_run_1> <num_of_messages_for_run_2> <num_of_messages_for_run_3> ...

'''

import json
import sys
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Check and save system argument
assert len(
    sys.argv) >= 2, "Performance calculator must take at least two parameter: name of the log file(s), and the number(s) of messages for each trial"
assert sys.argv[3] == 'throughput' or sys.argv[2] == 'latency', "Test type must be 'throughput' or 'latency'"

# Set constants
TEST_TYPE = sys.argv[2] if sys.argv[2] == 'latency' else sys.argv[3]
LOG_PATH = TEST_TYPE + '_logs/' + \
    sys.argv[1] if TEST_TYPE == 'latency' else None
WITH_SURB_LOG_PATH = TEST_TYPE + '_logs/' + \
    sys.argv[1] + '/with_surb/' if TEST_TYPE == 'throughput' else None
WITHOUT_SURB_LOG_PATH = TEST_TYPE + '_logs/' + \
    sys.argv[2] + '/without_surb/' if TEST_TYPE == 'throughput' else None


def calculate_latency(start_dict, end_dict):
    latency_arr = []
    for i in range(len(start_dict)):
        if str(i) in end_dict and str(i) and start_dict and end_dict[str(i)] > 0 and start_dict[str(i)] > 0:
            latency_arr.append(end_dict[str(i)] - start_dict[str(i)])
            #assert end_dict[str(i)] - start_dict[str(i)] > 0, i
    return np.array(latency_arr)


def plot_latency(arr):
    x_arr = [int(sys.argv.index(message_num)) - 3] * len(arr)
    plt.scatter(np.array(x_arr), arr)
    return x_arr


# Scatter plot trendline
def plot_best_fit(x, y):
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color='purple')
    return m*x + b


def calculate_throughput(data, tag, message_num):
    if tag in data:
        if tag == 'received_surb_time':
            return float(message_num) / float(data[tag][1])
        return float(message_num) / float(data[tag])


if TEST_TYPE == 'latency':
    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    # To draw the best fit lines for each graph, we need to accumulate the data from different runs. (Not a pretty or smart way, but OK for now)
    all_x_surb_reply_latency = []
    all_y_surb_reply_latency = []
    all_x_text_latency_without_surb = []
    all_y_text_latency_without_surb = []
    all_x_text_latency_with_surb = []
    all_y_text_latency_with_surb = []

    for message_num in sys.argv[3:]:
        with open(LOG_PATH + '/' + message_num + '/sender.json', 'r') as file:
            sender_data = json.load(file)

        with open(LOG_PATH + '/' + message_num + '/receiver.json', 'r') as file:
            receiver_data = json.load(file)

        # SURB Reply latency
        surb_reply_latency = calculate_latency(
            receiver_data['sent_surb_reply_text_time'], sender_data['received_surb_reply_text_time'])
        print('surb reply latency {}'.format(surb_reply_latency))

        # Uncomment for unfiltered boxplot OR table creation
        all_y_surb_reply_latency.append(list(surb_reply_latency))

        # Uncomment for filtered boxplot, if you would like to filter out the outputs to make the boxplot prettier
        # cutoff = 4
        # all_y_surb_reply_latency.append(
        #     [x for x in surb_reply_latency if x < cutoff])

        # Uncomment for scatter plot
        # all_y_surb_reply_latency += list(surb_reply_latency)
        # all_x_surb_reply_latency += plot_latency(surb_reply_latency)

        ####################################################
        # Text message (no SURB attached) latency
        text_latency_without_surb = calculate_latency(
            sender_data['sent_text_without_surb_time'], receiver_data['received_text_time'])

        # Uncomment for unfiltered boxplot OR table creation
        all_y_text_latency_without_surb.append(list(text_latency_without_surb))

        # Uncomment for filtered boxplot, if you would like to filter out the outputs to make the boxplot prettier
        # cutoff = 35
        # all_y_text_latency_without_surb.append(
        #     [x for x in text_latency_without_surb if x < cutoff])

        # Uncomment for scatter plot
        # all_y_text_latency_without_surb += list(text_latency_without_surb)
        # all_x_text_latency_without_surb += plot_latency(
        #     text_latency_without_surb)

        ####################################################
        # Text message (SURB attached) latency
        text_latency_with_surb = calculate_latency(
            sender_data['sent_text_with_surb_time'], receiver_data['received_surb_text_time'])

        # Uncomment for unfiltered boxplot OR table creation
        all_y_text_latency_with_surb.append(list(text_latency_with_surb))

        # Uncomment for filtered boxplot, if you would like to filter out the outputs to make the boxplot prettier
        # cutoff = 35
        # all_y_text_latency_with_surb.append(
        #     [x for x in text_latency_with_surb if x < cutoff])

        # Uncomment for scatter plot
        # all_y_text_latency_with_surb += list(text_latency_with_surb)
        # all_x_text_latency_with_surb += plot_latency(
        #     text_latency_with_surb)

    ##### GRAPHS #####
    # plt.grid(visible=True, axis='y')
    # # Modify according to the graph
    # plt.title("Text message (no SURB attached)")
    # plt.xlabel('Number of messages')
    # plt.ylabel('Latency per message (secs)')
    # plot_name = '/text-with-surb-unfiltered-scatterplot.png'

    # Uncomment and modify for boxplot
    # plt.boxplot(all_y_text_latency_with_surb, labels=sys.argv[3:])

    # Uncomment and modify for scatter plot
    # best_fit = plot_best_fit(np.array(all_x_text_latency_with_surb),
    #                          np.array(all_y_text_latency_with_surb))
    # plt.xticks(ticks=[0, 1, 2], labels=sys.argv[3:])
    # avg_best_fit = round(np.average(best_fit), 2)
    # plt.text(-0.28, avg_best_fit, avg_best_fit, color='purple', va='center')

    # plt.savefig(LOG_PATH + plot_name)

    ##### TABLES #####
    # Table structure is:
    #                       Average | StdDev | Min | Max | Loss
    # <msg type>_<msg num>
    # <msg type>_<msg num>
    #          ...

    def percentage(part, whole):
        return 100 * float(part)/float(whole)

    table = dict()
    table['Average'] = list()
    table['StdDev'] = list()
    table['Min'] = list()
    table['Max'] = list()
    table['Loss'] = list()
    table['Average'].extend(np.average(latency)
                            for latency in all_y_surb_reply_latency)
    table['Average'].extend(np.average(latency)
                            for latency in all_y_text_latency_with_surb)
    table['Average'].extend(np.average(latency)
                            for latency in all_y_text_latency_without_surb)
    table['StdDev'].extend(np.std(latency)
                           for latency in all_y_surb_reply_latency)
    table['StdDev'].extend(np.std(latency)
                           for latency in all_y_text_latency_with_surb)
    table['StdDev'].extend(np.std(latency)
                           for latency in all_y_text_latency_without_surb)
    table['Min'].extend(np.min(latency)
                        for latency in all_y_surb_reply_latency)
    table['Min'].extend(np.min(latency)
                        for latency in all_y_text_latency_with_surb)
    table['Min'].extend(np.min(latency)
                        for latency in all_y_text_latency_without_surb)
    table['Max'].extend(np.min(latency)
                        for latency in all_y_surb_reply_latency)
    table['Max'].extend(np.min(latency)
                        for latency in all_y_text_latency_with_surb)
    table['Max'].extend(np.min(latency)
                        for latency in all_y_text_latency_without_surb)
    table['Loss'].extend(percentage(len(all_y_surb_reply_latency[i]),
                                    sys.argv[3 + i])for i in range(len(all_y_surb_reply_latency)))
    table['Loss'].extend(percentage(len(all_y_text_latency_with_surb[i]),
                                    sys.argv[3 + i])for i in range(len(all_y_text_latency_with_surb)))
    table['Loss'].extend(percentage(len(all_y_text_latency_without_surb[i]),
                                    sys.argv[3 + i])for i in range(len(all_y_text_latency_without_surb)))
    df = pd.DataFrame(table, index=['SURB_100', 'SURB_1000', 'SURB_10000', 'Text_With_SURB_100', 'Text_With_SURB_1000',
                                    'Text_With_SURB_10000', 'Text_Without_SURB_100', 'Text_Without_SURB_1000', 'Text_Without_SURB_10000'])
    df.to_csv(LOG_PATH + '/table.csv')

# Throughput
else:
    sent_text_with_surb_time_y = []
    sent_text_with_surb_time_x = []
    sent_text_without_surb_time_y = []
    sent_text_without_surb_time_x = []
    received_surb_reply_time_y = []
    received_surb_reply_time_x = []

    received_surb_text_time_y = []
    received_surb_text_time_x = []
    received_text_time_y = []
    received_text_time_x = []
    sent_surb_reply_time_y = []
    sent_surb_reply_time_x = []

    logging.info("[PERFORMANCE_CALC] Throughput data:")
    for message_num in sys.argv[4:]:
        sender_data = dict()
        receiver_data = dict()
        with open(WITH_SURB_LOG_PATH + '/' + message_num + '/sender.json', 'r') as file:
            sender_data.update(json.load(file))

        with open(WITHOUT_SURB_LOG_PATH + '/' + message_num + '/sender.json', 'r') as file:
            sender_data.update(json.load(file))

        with open(WITH_SURB_LOG_PATH + '/' + message_num + '/receiver.json', 'r') as file:
            receiver_data.update(json.load(file))

        with open(WITHOUT_SURB_LOG_PATH + '/' + message_num + '/receiver.json', 'r') as file:
            receiver_data.update(json.load(file))

        sent_text_with_surb_time_y.append(calculate_throughput(
            sender_data, 'sent_text_with_surb_time', message_num))
        sent_text_with_surb_time_x.append(int(message_num))

        sent_text_without_surb_time_y.append(calculate_throughput(
            sender_data, 'sent_text_without_surb_time', message_num))
        sent_text_without_surb_time_x.append(int(message_num))

        received_surb_text_time_y.append(calculate_throughput(
            receiver_data, 'received_text_with_surb_time', message_num))
        received_surb_text_time_x.append(int(message_num))

        received_text_time_y.append(calculate_throughput(
            receiver_data, 'received_text_without_surb_time', message_num))
        received_text_time_x.append(int(message_num))

        sent_surb_reply_time_y.append(calculate_throughput(
            receiver_data, 'sent_surb_time', message_num))
        sent_surb_reply_time_x.append(int(message_num))

        received_surb_reply_time_y.append(calculate_throughput(
            sender_data, 'received_surb_time', sender_data['received_surb_time'][0]))
        received_surb_reply_time_x.append(sender_data['received_surb_time'][0])

    plt.plot(sent_text_with_surb_time_x, sent_text_with_surb_time_y,
             label='text message (SURB attached)')
    plt.plot(sent_text_without_surb_time_x, sent_text_without_surb_time_y,
             label='text message (no SURB attached)')
    plt.plot(sent_surb_reply_time_x, sent_surb_reply_time_y,
             label='reply message using SURB')
    plt.legend()
    plt.grid(visible=True, axis='y')
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.title('Throughput: Sending messages')
    plt.xlabel('Number of messages')
    plt.ylabel('Throughput (msg/sec)')
    ax = plt.gca()
    plt.xticks([100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500,
                5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000], rotation=90)
    plt.savefig(TEST_TYPE + '_logs/' + sys.argv[1] + '/sent_text_plot.png')

    plt.clf()

    plt.title('Throughput: Receiving messages')
    plt.plot(received_surb_text_time_x, received_surb_text_time_y,
             label='text message (SURB attached)')
    plt.plot(received_text_time_x, received_text_time_y,
             label='text message (no SURB attached)')
    plt.plot(received_surb_reply_time_x, received_surb_reply_time_y,
             label='reply message using SURB')
    plt.legend()
    plt.grid(visible=True, axis='y')
    plt.title('Throughput: Receiving messages')
    plt.xlabel('Number of messages')
    plt.ylabel('Throughput (msg/sec)')
    plt.xticks([100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500,
                5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000], rotation=90)
    plt.savefig(TEST_TYPE + '_logs/' + sys.argv[1] + '/received_text_plot.png')
