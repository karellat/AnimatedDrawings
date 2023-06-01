if __name__ == '__main__':
    # Load images
    img_b = cv2.imencode('.png', img)[1].tobytes()
    request_data = {'data': img_b}
    # Log POST
    print(request_data)
    resp = requests.post("http://localhost:8080/predictions/drawn_humanoid_detector", files=request_data, verify=False)
    # Test post

    # Show Gif
