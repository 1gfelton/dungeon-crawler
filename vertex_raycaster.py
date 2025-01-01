from cmu_graphics import *
from ray import *
from point import *

def drawRays(app):
    visPoints = []
    seen = set()
    player = Point(app.player.x, app.player.y)
    print('start raycast')
    for wall in app.walls:
        for point in wall.points:
            # don't check duplicate points
            if point in seen:
                continue
            # for each point, cast a ray from the player slightly left and right of the point
            angle = player.angleto(point)
            angLeft = angle + 0.001
            angRight = angle - 0.001
            # check intersection events for all walls
            rayLeft = Ray(player.x, player.y, angLeft)
            lClose, lDist = None, math.inf
            rayRight = Ray(player.x, player.y, angRight)
            rClose, rDist = None, math.inf
            for wall2 in app.walls:
                # get the closest intersection point for this ray
                lp = rayLeft.cast(wall2)
                lint = Point(lp[0], lp[1]) if lp else None
                if lint:
                    if player.dist(lint) < lDist:
                        lDist = player.dist(lint)
                        lClose = lint
                rp = rayRight.cast(wall2)
                rint = Point(rp[0], rp[1]) if rp else None
                if rint:
                    if player.dist(rint) < rDist:
                        rDist = player.dist(rint)
                        rClose = rint
            seen.add(point)
            # if lDist and rDist are closer than the dist to current point, the point is not visible
            visPoints.append((angLeft, lClose))
            visPoints.append((angRight, rClose))
    sortedPoints = sortPoints(app, visPoints)
    polygonPoints = []
    # get the points into something drawpolygon can use
    for point in sortedPoints:
        polygonPoints.extend([point.x, point.y])
    distances = [player.dist(point) for point in sortedPoints]
    print('dist:', distances)
    width = app.width/len(distances)
    # create the points of the wall polygons to draw
    drawPolygon(*polygonPoints, fill='yellow', opacity=50)

def sortPoints(app, points):
    seen = set()
    result = []
    player = Point(app.player.x, app.player.y)
    for angle, currentPoint in points:
        if currentPoint in seen:
            continue
        seen.add(currentPoint)
        adjustedAng = angle if angle >= 0 else angle + 2 * math.pi
        result.append((adjustedAng, currentPoint))
    sortedPoints = sorted(points, key=lambda point: point[0])
    result = [point[1] for point in sortedPoints]
    print('sorted points:', result)
    return result