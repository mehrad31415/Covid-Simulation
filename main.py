import numpy as np
import plotly.graph_objects as go
import pandas as pd
# import matplotlib.pyplot as plt
# import time

# We generate a start and an end point of a route
# n is the size of the map
def generate_start_and_end(n):
    start_point = (np.random.randint(0, n), np.random.randint(0, n))
    end_point = (np.random.randint(0, n), np.random.randint(0, n))
    return start_point, end_point

# Generate random points with this function
# n is size of map
def generate_random_point(n):
    return (np.random.randint(0, n), np.random.randint(0, n))

# We create a random route for walking from start to end as meaningful (without repeated edge walking and in minimum distance)
def generate_random_route(start, end):
    path = [(start[0], start[1])]
    now_point = [start[0], start[1]]
    while (now_point[0], now_point[1]) != end:
        if now_point[0] == end[0]:
            coin = 1
        elif now_point[1] == end[1]:
            coin = 0
        else:
            coin = np.random.randint(0,2)

        if coin == 0:
            if now_point[0] > end[0]:
                now_point[0] -= 1
            else:
                now_point[0] += 1
        else:
            if now_point[1] > end[1]:
                now_point[1] -= 1
            else:
                now_point[1] += 1
        path.append((now_point[0], now_point[1]))
    return path

# Generate all routes we need, n is number of routes
def generate_routes(n):
    routes = {}
    for i in range(n):
        start, end = generate_start_and_end(size_of_map)
        if start[0] == end[0]:
            if start[0] > (size_of_map / 2):
                start = (start[0] - size_of_map / 4, start[1])
            else:
                start = (start[0] + size_of_map / 4, start[1])
        
        if start[1] == end[1]:
            if start[1] > (size_of_map / 2):
                start = (start[0], start[1] - size_of_map / 4)
            else:
                start = (start[0], start[1] + size_of_map / 4)
        
        route = generate_random_route(start, end)
        routes[f"route-{i+1}"] = [start, end, route]
    return routes

# This is our core function. Here we get points and distance as length, all routes, and count and type of steps (or t parameter)
# and return name of path that have our condition
def determine_near_path(points, length, routes, steps, type_of_steps = None):
    name_of_routes = set()
    for point in points:
        neighbours = generate_neighbours_of_length_lower_that([point],length, [point])
        for i in routes:
            for j in neighbours:
                if type_of_steps == 'lower':
                    if j in routes[i][2][:steps]:
                        name_of_routes.add(i)
                elif type_of_steps == 'higher':
                    if j in routes[i][2][steps+1:]:
                        name_of_routes.add(i)
                elif type_of_steps == "exact":
                    if j in routes[i][2][steps]:
                        name_of_routes.add(i)
                else:
                    if j in routes[i][2]:
                        name_of_routes.add(i)
    return name_of_routes

# generate all neighbours of point p, with lower distance n
def generate_neighbours_of_length_lower_that(p, n, output):
    if n == 0:
        return p
    neighbours = []
    for i in p:
        right = (i[0]+1, i[1])
        if right[0] >= 0 and right[1] >= 0:
            neighbours.append(right)
        left = (i[0]-1, i[1])
        if left[0] >= 0 and left[1] >= 0:
            neighbours.append(left)
        up = (i[0], i[1]+1)
        if up[0] >= 0 and up[1] >= 0:
            neighbours.append(up)
        down = (i[0], i[1]-1)
        if down[0] >= 0 and down[1] >= 0:
            neighbours.append(down)
    if n > 1:
        result = generate_neighbours_of_length_lower_that(neighbours, n-1, p+output)
    else:
        result = neighbours + p
    return set(result)

# export as image
def save_image(points, routes,routes_detected):
    fig, ax = plt.subplots()
    ax.grid(True)
    for p in points:
        ax.scatter(p[0], p[1], s=25, color='blue', cmap=plt.cm.coolwarm, zorder=10)
    ax.scatter(0, 0, color='white')
    ax.scatter(size_of_map, size_of_map, color='white')
    for i in routes:
        x = [p[0] for p in routes[i][2]]
        y = [p[1] for p in routes[i][2]]
        if i in routes_detected:
            ax.plot(x, y, color="green", markevery=[0, -1], marker="x")
        else:
            ax.plot(x, y, color="red", linestyle="dashed", markevery=[0, -1], marker="o")
    fig.savefig('so.png', dpi=1200)

# export as html file
def export_interactive(points, routes,routes_detected):
    fig = go.Figure()
    fig.update_layout(
        width=800,
        height=800
    )
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1
    )
    point_counter = 1
    for p in points:
        fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode='markers', name=f'random point - {point_counter}', marker_color='rgba(100, 100, 255, .9)'))
        point_counter += 1

    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker_color='rgba(255, 255, 255, .01)',showlegend=False))
    fig.add_trace(go.Scatter(x=[size_of_map], y=[size_of_map], mode='markers', marker_color='rgba(255, 255, 255, .01)',showlegend=False))

    for i in routes:
        x = [p[0] for p in routes[i][2]]
        y = [p[1] for p in routes[i][2]]
        if i in routes_detected:
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=i, marker_color='rgba(50, 255, 0, .9)'))
        else:
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=i, marker_color='rgba(255, 50, 0, .9)'))
    fig.write_html("export.html")

# export excel file
def export_excel_data(routes, routes_detected):
    df = pd.DataFrame()
    for i in routes:
        df[i] = pd.Series(routes[i][2])
    
    writer = pd.ExcelWriter("export.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    cell_format = workbook.add_format({'bg_color': '#32b945'})

    for col_num, col_name in enumerate(df.columns.values):
        if col_name in routes_detected:
            worksheet.write(0, col_num + 1, col_name)
            worksheet.set_column(col_num + 1,col_num + 1, 20, cell_format)
        else:
            worksheet.write(0, col_num + 1, col_name)
            worksheet.set_column(col_num + 1,col_num + 1, 20)
    writer.save()


def main():
    points = set([generate_random_point(size_of_map) for i in range(number_of_points)])
    
    routes = generate_routes(number_of_routes)

    # route_by_hand
    # print(routes)
    routes["root-by-hand-1"]=[(0,0),(1,2),[(0,0),(0,1),(1,1),(1,2)]]

    
    routes_detected = determine_near_path(points, distance, routes, number_of_steps, type_of_steps)
    
     # save_image(p, routes, routes_detected)
    export_interactive(points, routes, routes_detected)
    
    export_excel_data(routes, routes_detected)




if __name__ == "__main__":
    # now = time.time()

    size_of_map = 500 # size of XY plane (or size of map)

    number_of_points = 10 # number of custom random points

    number_of_routes = 100 # number of custom random routes

    distance = 3 # distance between two point (sum of edges)

    number_of_steps = 5 # t parameter
    type_of_steps = "higher" # lower / exact / higher / None

    main()
    
    # print(time.time() - now)
