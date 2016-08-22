import math
from svg import SVGElement, SVGRoot
from elements import Line, Text, Transform
from collect_data import collect_data

def main():

  # raw_data = collect_data(file)
  raw_data = collect_data()
 
  x_times = raw_data['calls'][0]['24-11']['forward']['frame-arrival'] 
  data = raw_data['calls'][0]['24-11']['forward']['jitter']

  margin = {
    "top"    : 40,
    "left"   : 70,
    "right"  : 70,
    "bottom" : 40
  }

  width = 800
  height = 450
  graph_width = width - (margin['left'] + margin['right'])
  graph_height = height - (margin['top'] + margin['bottom'])
  x_baseline = height - margin['bottom']
  y_baseline = margin['left']
  tick_length = 5

  root = SVGRoot(width, height)
  root.style({
    # "svg": {
    #   "border": "1px solid #000"
    # },
    "text": {
      "font": "11px Verdana, Helvetica, Arial, sans-serif",
      "color": "#f00"
    }
  })

  x_axis = Line(margin['left'], width - margin['right'], x_baseline, x_baseline)
  root.add(x_axis)

  y_axis = Line(margin['left'], margin['left'], margin['top'], x_baseline)
  root.add(y_axis)

  # ticks
  num_data_points = len(data) + 1
  tick_space = float(graph_width) / 10

  # x-ticks
  for i in range(0, 11):
    tick_point = (i * tick_space) + margin['left']
    tick = Line(tick_point, tick_point, x_baseline, x_baseline + tick_length)
    root.add(tick)

  # x-labels
  times_count = len(x_times)
  step = times_count / 10
  j = 0
  dy = 0.75

  for i in range(0, times_count, step):
    label_text = "%.2f" % (x_times[i] - x_times[0])
    tick_point = (j * tick_space) + margin['left']
    label = Text(label_text, tick_point, x_baseline + tick_length, 0, dy)
    root.add(label)
    j += 1

  tick_point = (j * tick_space) + margin['left']
  label_text = "%.2f" % (x_times[len(x_times) - 1] - x_times[0])
  label = Text(label_text, tick_point, x_baseline + tick_length, 0, dy)
  root.add(label)

  x_title = Text("Arrival (ms)", (graph_width / 2) + margin['left'], height - (margin['bottom'] / 2) + 10)
  root.add(x_title)

  # summary
  data_max = max(data)
  data_min = min(data)
  data_total = sum(data)
  data_mean = data_total / len(data)

  # y-ticks
  range_top = (data_max / 4) * 5
  range_top = int(math.ceil(range_top / 10.0) * 10)

  tick_count = (range_top - (range_top % 10)) / 10
  tick_space = float(graph_height) / tick_count
  dy = 0.33

  for i in range(0, int(tick_count) + 1):
    tick_point = (i * tick_space) + margin['top']
    tick = Line(y_baseline - tick_length, y_baseline, tick_point, tick_point)
    label_text = "%.2f" % (range_top - ((range_top / tick_count) * i))
    label = Text(label_text, y_baseline - tick_length, tick_point, 0, dy)
    label.anchorEnd()
    root.add(tick)
    root.add(label)

  y_title = Text("Jitter (ms)", (margin['left'] / 3.5), (graph_height / 2) + margin['top'])
  transform = Transform()
  transform.rotate(degrees = 270, x = (margin['left'] / 3.5), y = (graph_height / 2) + margin['top'])
  y_title.transform(transform)
  root.add(y_title)

  # place data
  tick_space = float(graph_width) / num_data_points
  data_unit = float(graph_height) / range_top
  for i in range(1, num_data_points):
    tick_point = (i * tick_space) + margin['left']
    y_point = data[i - 1] * data_unit
    data_mark = Line(tick_point, tick_point, x_baseline, x_baseline - y_point)
    root.add(data_mark)

  # max line
  data_max_plot = margin['top'] + (range_top - data_max) * data_unit
  max_line = Line(margin['left'], width - margin['right'] + 10, data_max_plot, data_max_plot)
  max_line.stroke(stroke="red")
  max_label = Text("%.2fms" % data_max, width - margin['right'] + 10, data_max_plot, dx=0.5, dy=0.33)
  max_label.anchorStart()
  root.add(max_line)
  root.add(max_label)

  # mean line
  data_mean_plot = margin['top'] + (range_top - data_mean) * data_unit
  mean_line = Line(margin['left'], width - margin['right'] + 10, data_mean_plot, data_mean_plot)
  mean_line.stroke(stroke="blue")
  mean_label = Text("%.2fms" % data_mean, width - margin['right'] + 10, data_mean_plot, dx=0.5, dy=0.33)
  mean_label.anchorStart()
  root.add(mean_line)
  root.add(mean_label)

  # min line
  data_min_plot = margin['top'] + (range_top - data_min) * data_unit
  min_line = Line(margin['left'], width - margin['right'] + 10, data_min_plot, data_min_plot)
  min_line.stroke(stroke="green")
  min_label = Text("%.2fms" % data_min, width - margin['right'] + 10, data_min_plot, dx=0.5, dy=0.33)
  min_label.anchorStart()
  root.add(min_line)
  root.add(min_label)

  svg = root.render()

  with open('file.svg', 'w') as file:
    file.write(svg)
    file.close()

if __name__ == "__main__":
  main()
