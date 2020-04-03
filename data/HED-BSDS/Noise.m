function y=Noise(Image,nbLook)
        s = zeros(size(Image));
        for k = 1:nbLook
            s = s + abs(randn(size(Image)) + i * randn(size(Image))).^2 / 2;
        end
        y = Image .* sqrt(s / nbLook);
        