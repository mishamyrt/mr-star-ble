"""Enum block tests"""
import pytest

from mr_star_ble.commands import (
    format_brightness_command,
    format_color_command,
    format_command,
    format_effect_command,
    format_length_command,
    format_power_command,
    format_reverse_command,
    format_speed_command,
)
from mr_star_ble.const import Command, Effect


def test_format_command():
    """Test base command formatting"""
    assert format_command(Command.SET_POWER, [0x02, 0x03]) == bytes([
        0xBC, 0x01, 0x02, 0x02, 0x03, 0x55])
    try:
        format_command(Command.SET_POWER, [])
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True

def test_format_power_command():
    """Test power command formatting"""
    assert format_power_command(True) == bytes([
        0xBC, 0x01, 0x01, 0x01, 0x55])
    assert format_power_command(False) == bytes([
        0xBC, 0x01, 0x01, 0x00, 0x55])

def test_format_brightness_command():
    """Test brightness command formatting"""
    assert format_brightness_command(0) == bytes([
        0xBC, 0x05, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])
    assert format_brightness_command(1) == bytes([
        0xBC, 0x05, 0x06, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])
    assert format_brightness_command(0.5) == bytes([
        0xBC, 0x05, 0x06, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])

    try:
        format_brightness_command(2)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
    try:
        format_brightness_command(-1)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True


def test_format_color_command():
    """Test color command formatting"""
    assert format_color_command((0, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0x00, 0x03, 0xe8, 0x00, 0x00, 0x55])
    assert format_color_command((120, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0x78, 0x03, 0xE8, 0x00, 0x00, 0x55])
    assert format_color_command((240, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0xF0, 0x03, 0xE8, 0x00, 0x00, 0x55])

def test_format_reverse_command():
    """Test reverse command formatting"""
    assert format_reverse_command(True) == bytes([
        0xBC, 0x07, 0x01, 0x01, 0x55])
    assert format_reverse_command(False) == bytes([
        0xBC, 0x07, 0x01, 0x00, 0x55])

def test_format_speed_command():
    """Test speed command formatting"""
    assert format_speed_command(0.01) == bytes([
        0xBC, 0x08, 0x01, 0x01, 0x55])
    assert format_speed_command(0.5) == bytes([
        0xBC, 0x08, 0x01, 0x32, 0x55])
    assert format_speed_command(1) == bytes([
        0xBC, 0x08, 0x01, 0x64, 0x55])
    try:
        format_speed_command(2)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
    try:
        format_speed_command(-1)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True

def test_format_effect_command():
    """Test effect command formatting"""
    assert format_effect_command(Effect.AUTOMATIC_LOOP) == bytes([
        0xBC, 0x06, 0x02, 0x00, 0x01, 0x55])
    assert format_effect_command(Effect.SYMPHONY) == bytes([
        0xBC, 0x06, 0x02, 0x00, 0x02, 0x55])
    assert format_effect_command(Effect.PURPLE_OPEN_CLOSE) == bytes([
        0xBC, 0x06, 0x02, 0x00, 0x2B, 0x55])

def test_format_length_command():
    """Test length command formatting"""
    assert format_length_command(8) == bytes([
        0xBC, 0x03, 0x02, 0x00, 0x08, 0x55])
    assert format_length_command(255) == bytes([
        0xBC, 0x03, 0x02, 0x00, 0xFF, 0x55])
    assert format_length_command(300) == bytes([
        0xBC, 0x03, 0x02, 0x01, 0x2C, 0x55])
    try:
        format_length_command(7)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
    try:
        format_length_command(301)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
