import cv2 as cv
import numpy as np


def getPlayerCharacter(image, area, threshold=0.7, zoom=1):
    """
    get the character of the player in the specified area
    try to match the template of the lord, if the match is successful, the player is the lord, otherwise a farmer
    :param image:
    :param area:
    :param threshold:
    :param zoom:
    :return: whether the player is the lord
    """
    x1 = int(image.shape[1] * area[0])
    y1 = int(image.shape[0] * area[1])
    x2 = int(image.shape[1] * area[2])
    y2 = int(image.shape[0] * area[3])
    image = cv.resize(image, (int(image.shape[1] * zoom), int(image.shape[0] * zoom)))

    image = image[y1:y2, x1:x2]

    # cv.imshow('image', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    template = cv.imread('Vision_Part/templates/lord.jpg', cv.IMREAD_GRAYSCALE)

    result = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    return len(locations) > 0


def getCardsInArea(image, area, ratio=1, threshold=0.55, zoom=0.5):
    """
    modify area to specify an area to recognize,
    modify ratio if the template is not the same size as the card
    this is designed to fit different size of cards in different areas;
    the referred templates are in the templates folder;
    here we convert the image into a gray one while matching cards except the jokers,
    because we need to split the red joker and the black joker apart by color

    :param image: the origin image to process, colored image
    :param area: (x1, x2, y1, y2) map the origin size to 0~1 then use these fraction to specify the area
    :param ratio: the ratio of the template to the card, to match different size of cards
    :param threshold: the threshold of the matchTemplate
    :param zoom: the total zoom rate, 0.4 will not cause wrong matches and improve the match speed(an average of 0.4s)
    :return: a list to represent the deck
    """
    ratio *= zoom

    image = cv.resize(image, (int(image.shape[1] * zoom), int(image.shape[0] * zoom)))
    x1 = int(image.shape[1] * area[0])
    y1 = int(image.shape[0] * area[1])
    x2 = int(image.shape[1] * area[2])
    y2 = int(image.shape[0] * area[3])

    deck = [0] * 15
    image = image[y1:y2, x1:x2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # cards are in the order of 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A, 2, black joker, red joker
    for i in range(15):
        template = cv.imread('C:\\Users\\21525\\Desktop\\Pork\\Pork_Python\\Vision_Part\\templates\\' + str(i) + '.jpg')
        template = cv.resize(template, (int(template.shape[1] * ratio), int(template.shape[0] * ratio)))
        if i >= 13:
            # here we use the colored image to match the jokers
            result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
        else:
            template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
            result = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)

        # filter the result by threshold
        locations = np.where(result >= threshold)
        # zip the locations to a list of tuples, which is the left top corner of the matched area
        locations = list(zip(*locations[::-1]))

        locations = remove_duplicates(locations)

        deck[i] += len(locations)

    return deck


def getCardPosition(image, rank, threshold=0.95, zoom=0.5):
    """
    similar to the function getCardsInArea without looping
    return clickable positions of the cards with the specified rank
    :param image:
    :param rank:
    :param threshold:
    :param zoom:
    :return:
    """
    template = cv.imread('Vision_Part/templates/' + str(rank) + '.jpg')
    template = cv.resize(template, (int(template.shape[1] * zoom), int(template.shape[0] * zoom)))

    x1 = int(image.shape[1] * 0)
    y1 = int(image.shape[0] * 1 / 2)
    x2 = int(image.shape[1] * 1)
    y2 = int(image.shape[0] * 1)

    image = image[y1:y2, x1:x2]
    image = cv.resize(image, (int(image.shape[1] * zoom), int(image.shape[0] * zoom)))

    if rank >= 13:
        result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    else:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    locations = remove_duplicates(locations)

    locations = [(int((i[0] + 5) / zoom), int((i[1] + 5) / zoom + y1)) for i in locations]
    return locations


def getButtonPosition(image, button, threshold=0.8, zoom=0.5):
    """
    similar to the function getCardPosition
    :param image:
    :param button:
    :param threshold:
    :param zoom:
    :return:
    """
    template = cv.imread('Vision_Part/templates/' + button + '.jpg')
    template = cv.resize(template, (int(template.shape[1] * zoom), int(template.shape[0] * zoom)))
    # cv.imshow('t',template)


    x1 = int(image.shape[1] * 0)
    y1 = int(image.shape[0] * 1 / 2)
    x2 = int(image.shape[1] * 1)
    y2 = int(image.shape[0] * 1)

    image = image[y1:y2, x1:x2]
    image = cv.resize(image, (int(image.shape[1] * zoom), int(image.shape[0] * zoom)))
    result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    locations = remove_duplicates(locations)

    locations = [(int((i[0] + 5) / zoom), int((i[1] + 5) / zoom + y1)) for i in locations]
    return locations


def remove_duplicates(locations):
    """
    remove the duplicates in locations
    match result in the function above will return many duplicates or very close ones that all fit the threshold
    but to count the amount of different ranks we need only one of them
    :param locations:
    :return:
    """
    unique_locations = []
    for loc in locations:
        is_unique = True
        for unique_loc in unique_locations:
            if abs(loc[0] - unique_loc[0]) < 5 and abs(loc[1] - unique_loc[1]) < 5:
                is_unique = False
                break
        if is_unique:
            unique_locations.append(loc)
    return unique_locations
